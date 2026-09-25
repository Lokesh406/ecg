from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Text, DateTime

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ECGAnalysis(Base):
    __tablename__ = "ecg_analysis"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    s3_path = Column(String(500), nullable=True)
    heart_rate = Column(Float, nullable=True)
    peak_count = Column(Integer, nullable=True)
    mean_value = Column(Float, nullable=True)
    std_value = Column(Float, nullable=True)
    classification = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ProteinAnalysis(Base):
    __tablename__ = "protein_analysis"

    id = Column(Integer, primary_key=True, index=True)
    protein_name = Column(String(255), nullable=False)
    sequence = Column(Text, nullable=False)
    s3_path = Column(String(500), nullable=True)
    sequence_length = Column(Integer, nullable=True)
    molecular_weight = Column(Float, nullable=True)
    hydrophobicity = Column(Float, nullable=True)
    secondary_structure = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(50), nullable=False)
    related_id = Column(Integer, nullable=True)
    file_name = Column(String(255), nullable=False)
    s3_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
