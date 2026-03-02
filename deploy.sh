#!/bin/bash
# ============================================================
# deploy.sh — One-command deployment script for Linux server
# Usage: bash deploy.sh
# ============================================================

set -e  # Exit immediately if any command fails

echo ""
echo "=========================================="
echo "  Alphabit AI PDF Engine — Deploy Script  "
echo "=========================================="
echo ""

# ---------- 1. Check prerequisites ----------
echo "[1/5] Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed. Install it first:"
    echo "  https://docs.docker.com/engine/install/ubuntu/"
    exit 1
fi

if ! command -v docker compose &> /dev/null 2>&1; then
    # Try legacy docker-compose
    if ! command -v docker-compose &> /dev/null; then
        echo "ERROR: Docker Compose is not installed."
        echo "  Install: sudo apt-get install docker-compose-plugin"
        exit 1
    fi
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

echo "   Docker OK"
echo "   Docker Compose OK (using: $COMPOSE_CMD)"

# ---------- 2. Setup .env file ----------
echo ""
echo "[2/5] Checking .env file..."

if [ ! -f ".env" ]; then
    echo "   .env not found. Copying from .env.example..."
    cp .env.example .env
    echo "   DONE: .env created. Edit it if needed before running again."
else
    echo "   .env already exists. Using existing file."
fi

# ---------- 3. Stop old container (if running) ----------
echo ""
echo "[3/5] Stopping any running containers..."
$COMPOSE_CMD down --remove-orphans 2>/dev/null || true
echo "   Done."

# ---------- 4. Build and start ----------
echo ""
echo "[4/5] Building Docker image and starting container..."
$COMPOSE_CMD up --build -d

# ---------- 5. Health check ----------
echo ""
echo "[5/5] Waiting for app to be ready..."
sleep 5

MAX_RETRIES=10
COUNT=0
until curl -sf http://localhost:8000/ > /dev/null 2>&1; do
    COUNT=$((COUNT + 1))
    if [ $COUNT -ge $MAX_RETRIES ]; then
        echo "   WARNING: App did not respond after $MAX_RETRIES attempts."
        echo "   Check logs: $COMPOSE_CMD logs invoice-engine"
        break
    fi
    echo "   Waiting... ($COUNT/$MAX_RETRIES)"
    sleep 3
done

echo ""
echo "=========================================="
echo "  Deployment complete!"
echo "  App is running at: http://$(hostname -I | awk '{print $1}'):8000"
echo ""
echo "  Useful commands:"
echo "    View logs  :  $COMPOSE_CMD logs -f invoice-engine"
echo "    Stop app   :  $COMPOSE_CMD down"
echo "    Restart    :  $COMPOSE_CMD restart invoice-engine"
echo "=========================================="
echo ""
