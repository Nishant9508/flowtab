#!/bin/bash

echo "# Proof for Slice 1b" > docs/proof/slice1b.md

echo "## 1. Test Suite Full Run" >> docs/proof/slice1b.md
cd backend && PYTHONPATH=$(pwd) python3 -m pytest -v >> ../docs/proof/slice1b.md || true
cd ..

echo "## 2. Docker Compose Build and Up" >> docs/proof/slice1b.md
docker compose down || true
docker compose build >> docs/proof/slice1b.md 2>&1

echo "Starting DB..."
docker compose up -d db >> docs/proof/slice1b.md 2>&1
sleep 5

echo "Starting matching services..."
docker compose up -d >> docs/proof/slice1b.md 2>&1

echo "Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8080/openapi.json > /dev/null; then
        echo "Backend is up."
        break
    fi
    sleep 2
done

echo "## 3. Endpoints Output" >> docs/proof/slice1b.md
echo -e "\n### POST /api/v1/demo/generate\n\`\`\`json" >> docs/proof/slice1b.md
curl -s -X POST http://localhost:8080/api/v1/demo/generate -H "Content-Type: application/json" -d '{}' >> docs/proof/slice1b.md || true
echo -e "\n\`\`\`" >> docs/proof/slice1b.md

for EP in summary charges flow-graph architecture reconciliation coverage findings setup/checks; do
    echo -e "\n### GET /api/v1/network/$EP\n\`\`\`json" >> docs/proof/slice1b.md
    curl -s http://localhost:8080/api/v1/network/$EP >> docs/proof/slice1b.md || true
    echo -e "\n\`\`\`" >> docs/proof/slice1b.md
done

echo -e "\n### GET /api/v1/network/flows\n\`\`\`json" >> docs/proof/slice1b.md
curl -s http://localhost:8080/api/v1/network/flows >> docs/proof/slice1b.md || true
echo -e "\n\`\`\`" >> docs/proof/slice1b.md

docker compose down || true


