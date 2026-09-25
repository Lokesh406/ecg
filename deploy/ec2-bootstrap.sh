#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/your-user/cloud-science-platform.git}"

sudo apt-get update
sudo apt-get install -y ca-certificates curl git gnupg lsb-release

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker "$USER"

cd /home/ubuntu
if [ ! -d cloud-science-platform ]; then
  git clone "$REPO_URL" cloud-science-platform
fi

cd /home/ubuntu/cloud-science-platform

cp -n backend/.env.production.example backend/.env
cp -n frontend/.env.production.example frontend/.env.production

# Update these values before starting the app:
# nano backend/.env
# nano frontend/.env.production

echo "Next steps:"
echo "  1. Edit backend/.env and set DATABASE_URL, AWS credentials, and ALLOWED_ORIGINS"
echo "  2. Edit frontend/.env.production and set VITE_API_URL to your EC2/public API URL"
echo "  3. Run: docker compose up -d --build"

sudo docker compose up -d --build
