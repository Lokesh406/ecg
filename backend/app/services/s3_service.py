from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

from app.config import AWS_REGION, AWS_S3_BUCKET_NAME, BASE_DIR


class S3Service:
    def __init__(self) -> None:
        self.region = AWS_REGION
        self.bucket_name = AWS_S3_BUCKET_NAME
        self.local_root = BASE_DIR / "data" / "cloud_storage"
        self.local_root.mkdir(parents=True, exist_ok=True)
        self.client = None

        aws_access_key_id = (os.getenv("AWS_ACCESS_KEY_ID") or "").strip()
        aws_secret_access_key = (os.getenv("AWS_SECRET_ACCESS_KEY") or "").strip()
        aws_session_token = (os.getenv("AWS_SESSION_TOKEN") or "").strip()
        bucket_name = (self.bucket_name or "").strip()
        placeholder_prefixes = ("your-", "changeme", "example", "placeholder")

        configured = (
            bool(bucket_name)
            and bool(aws_access_key_id)
            and bool(aws_secret_access_key)
            and not any(
                aws_access_key_id.lower().startswith(prefix) or aws_secret_access_key.lower().startswith(prefix)
                for prefix in placeholder_prefixes
            )
        )

        if not configured:
            return

        try:
            self.client = boto3.client(
                "s3",
                region_name=self.region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token or None,
            )
            self.client.head_bucket(Bucket=bucket_name)
        except (BotoCoreError, ClientError, NoCredentialsError):
            self.client = None

    def _local_path_for(self, folder: str, file_name: str) -> Path:
        safe_folder = folder.strip("/")
        target_dir = self.local_root / safe_folder
        target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir / file_name

    def upload_file(self, file_name: str, file_bytes: bytes, folder: str) -> str:
        if self.client is None:
            local_file = self._local_path_for(folder, file_name)
            local_file.write_bytes(file_bytes)
            return f"file://{local_file.as_posix()}"

        try:
            key = f"{folder}/{file_name}"
            self.client.put_object(Bucket=self.bucket_name, Key=key, Body=file_bytes)
            return f"s3://{self.bucket_name}/{key}"
        except (BotoCoreError, ClientError) as exc:
            local_file = self._local_path_for(folder, file_name)
            local_file.write_bytes(file_bytes)
            return f"file://{local_file.as_posix()}"

    def download_file(self, key: str) -> bytes:
        if self.client is None:
            local_file = self.local_root / key
            return local_file.read_bytes()

        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=key)
            return response["Body"].read()
        except (BotoCoreError, ClientError) as exc:
            local_file = self.local_root / key
            return local_file.read_bytes()

    def list_files(self, prefix: str = "") -> list[str]:
        if self.client is None:
            base = self.local_root / prefix
            if not base.exists():
                return []
            return [str(p.relative_to(self.local_root)).replace('\\', '/') for p in base.rglob('*') if p.is_file()]

        try:
            response = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            contents = response.get("Contents", [])
            return [item["Key"] for item in contents]
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f"S3 list failed: {exc}") from exc
