#!/bin/bash

echo "# Proof for Slice 1" > docs/proof/slice1.md

echo "## 1. Test Suite Full Run" >> docs/proof/slice1.md
cd backend && PYTHONPATH=$(pwd) python3 -m pytest -v >> ../docs/proof/slice1.md || true
cd ..

echo "## 2. Docker Compose Build and Up" >> docs/proof/slice1.md
docker compose down -v || true
docker compose build >> docs/proof/slice1.md 2>&1
docker compose up -d >> docs/proof/slice1.md 2>&1

echo "Waiting for services to be ready..."
sleep 10

echo "## 3. Endpoints Output" >> docs/proof/slice1.md
echo -e "\n### POST /api/v1/demo/generate\n\`\`\`json" >> docs/proof/slice1.md
curl -s -X POST http://localhost:8080/api/v1/demo/generate -H "Content-Type: application/json" -d '{}' >> docs/proof/slice1.md || true
echo -e "\n\`\`\`" >> docs/proof/slice1.md

for EP in summary charges flow-graph architecture reconciliation coverage findings setup/checks; do
    echo -e "\n### GET /api/v1/network/$EP\n\`\`\`json" >> docs/proof/slice1.md
    curl -s http://localhost:8080/api/v1/network/$EP >> docs/proof/slice1.md || true
    echo -e "\n\`\`\`" >> docs/proof/slice1.md
done

echo -e "\n### GET /api/v1/network/flows (truncated)\n\`\`\`json" >> docs/proof/slice1.md
curl -s http://localhost:8080/api/v1/network/flows | head -c 500 >> docs/proof/slice1.md || true
echo -e "\n...\n\`\`\`" >> docs/proof/slice1.md

docker compose down -v || true


