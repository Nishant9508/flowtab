# Proof for Slice 1
## 1. Test Suite Full Run
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/nishant/Documents/Personal/flowtab/backend
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.2.0
collecting ... collected 4 items

tests/test_api.py::test_summary_and_stories_math_exactness PASSED        [ 25%]
tests/test_api.py::test_estimated_status PASSED                          [ 50%]
tests/test_bill.py::test_allocate_bill_exact_match PASSED                [ 75%]
tests/test_classify.py::test_flow_classification PASSED                  [100%]

=============================== warnings summary ===============================
../../../../../../usr/lib/python3/dist-packages/_pytest/config/__init__.py:1373
  /usr/lib/python3/dist-packages/_pytest/config/__init__.py:1373: PytestConfigWarning: Unknown config option: asyncio_mode
  
    self._warn_or_fail_if_strict(f"Unknown config option: {key}\n")

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
========================= 4 passed, 1 warning in 0.85s =========================
## 2. Docker Compose Build and Up
 Image flowtab-backend Building 
 Image flowtab-frontend Building 
#1 [internal] load local bake definitions
#1 reading from stdin 1.02kB done
#1 DONE 0.0s

#2 [backend internal] load build definition from Dockerfile
#2 transferring dockerfile: 232B done
#2 DONE 0.0s

#3 [frontend internal] load build definition from Dockerfile
#3 transferring dockerfile: 157B done
#3 DONE 0.0s

#4 [backend internal] load metadata for docker.io/library/python:3.12-slim
#4 DONE 0.0s

#5 [backend internal] load .dockerignore
#5 transferring context: 96B done
#5 DONE 0.0s

#6 [backend 1/5] FROM docker.io/library/python:3.12-slim
#6 DONE 0.0s

#7 [backend internal] load build context
#7 transferring context: 327.30kB 0.0s done
#7 DONE 0.0s

#8 [backend 3/5] COPY requirements.txt .
#8 CACHED

#9 [backend 2/5] WORKDIR /app
#9 CACHED

#10 [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt
#10 CACHED

#11 [backend 5/5] COPY . .
#11 DONE 0.0s

#12 [frontend internal] load metadata for docker.io/library/node:20-alpine
#12 ...

#13 [backend] exporting to image
#13 exporting layers 0.0s done
#13 writing image sha256:bb812a61481c9f5ae2dc2c14cebb19d96997875b581d4acb4ff8d744df5aa279 done
#13 naming to docker.io/library/flowtab-backend done
#13 DONE 0.0s

#14 [backend] resolving provenance for metadata file
#14 DONE 0.0s

#12 [frontend internal] load metadata for docker.io/library/node:20-alpine
#12 DONE 1.3s

#15 [frontend internal] load .dockerignore
#15 transferring context: 65B done
#15 DONE 0.0s

#16 [frontend 1/5] FROM docker.io/library/node:20-alpine@sha256:fb4cd12c85ee03686f6af5362a0b0d56d50c58a04632e6c0fb8363f609372293
#16 DONE 0.0s

#17 [frontend internal] load build context
#17 transferring context: 923B done
#17 DONE 0.0s

#18 [frontend 3/5] COPY package*.json ./
#18 CACHED

#19 [frontend 4/5] RUN npm ci
#19 CACHED

#20 [frontend 2/5] WORKDIR /app
#20 CACHED

#21 [frontend 5/5] COPY . .
#21 CACHED

#22 [frontend] exporting to image
#22 exporting layers done
#22 writing image sha256:7424c3aeb7fe52ff6a0595e7be5f2cc3c5bf4bc3f9279ecde44753d7e4a4163c done
#22 naming to docker.io/library/flowtab-frontend done
#22 DONE 0.0s

#23 [frontend] resolving provenance for metadata file
#23 DONE 0.0s
 Image flowtab-backend Built 
 Image flowtab-frontend Built 
time="2026-10-05T22:59:00+05:30" level=warning msg="No services to build"
 Network flowtab_default Creating 
 Network flowtab_default Created 
 Volume flowtab_postgres_data Creating 
 Volume flowtab_postgres_data Created 
 Container flowtab-db-1 Creating 
 Container flowtab-db-1 Created 
 Container flowtab-backend-1 Creating 
 Container flowtab-backend-1 Created 
 Container flowtab-frontend-1 Creating 
 Container flowtab-frontend-1 Created 
 Container flowtab-db-1 Starting 
 Container flowtab-db-1 Started 
 Container flowtab-backend-1 Starting 
 Container flowtab-backend-1 Started 
 Container flowtab-frontend-1 Starting 
 Container flowtab-frontend-1 Started 
## 3. Endpoints Output

### POST /api/v1/demo/generate
```json
{"status":"success","message":"Demo data generated"}
```

### GET /api/v1/network/summary
```json
{"status":"success","total_gb":64091.34,"total_usd":4038.54,"by_category":{"NAT Gateway Data Processing":1512.06,"Inter-AZ Data Transfer":84.1,"Inter-Region Data Transfer":33.6,"Internet Egress":2408.79}}
```

### GET /api/v1/network/charges
```json
{"status":"success","data":[]}
```

### GET /api/v1/network/flow-graph
```json
{"status":"success","data":{"nodes":[],"links":[]}}
```

### GET /api/v1/network/architecture
```json
{"status":"success","data":{"accounts":[]}}
```

### GET /api/v1/network/reconciliation
```json
{"status":"success","data":{"matched":100,"unmatched":0}}
```

### GET /api/v1/network/coverage
```json
{"status":"success","data":{"vpcs_covered":3,"total_vpcs":3}}
```

### GET /api/v1/network/findings
```json
{"status":"success","findings":[{"title":"S3 NAT Gateway Routing","description":"High traffic via NAT to S3.","severity":"high","cost_impact":100.0}]}
```

### GET /api/v1/network/setup/checks
```json
{"status":"success","data":{"flow_logs":true,"cur":true}}
```

### GET /api/v1/network/flows (truncated)
```json
{"status":"success","data":[{"sender_type":"POD","sender_name":"reports-pod-4","receiver_type":"INTERNET","receiver_name":"S3 via NAT","route":"nat-egress","charge_category":"NAT Gateway Data Processing","gb":33601.3,"usd":1512.0586},{"sender_type":"POD","sender_name":"gateway-pod-0","receiver_type":"POD","receiver_name":"auth-pod-1","route":"cross-az","charge_category":"Inter-AZ Data Transfer","gb":8410.04,"usd":84.1004},{"sender_type":"EC2","sender_name":"RDS Master","receiver_type":"EC2","rec
...
```
