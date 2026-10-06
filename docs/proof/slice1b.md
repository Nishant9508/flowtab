# Proof for Slice 1b
## 1. Test Suite Full Run
[1m============================= test session starts ==============================[0m
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/nishant/Documents/Personal/flowtab/backend
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.2.0
[1mcollecting ... [0mcollected 11 items

tests/test_api.py::test_api_summary_and_docs_match [32mPASSED[0m[32m                [  9%][0m
tests/test_api.py::test_api_findings_dynamic [32mPASSED[0m[32m                      [ 18%][0m
tests/test_api.py::test_api_charges [32mPASSED[0m[32m                               [ 27%][0m
tests/test_api.py::test_api_flow_graph [32mPASSED[0m[32m                            [ 36%][0m
tests/test_api.py::test_api_architecture [32mPASSED[0m[32m                          [ 45%][0m
tests/test_api.py::test_api_reconciliation [32mPASSED[0m[32m                        [ 54%][0m
tests/test_api.py::test_api_summary_filters_and_sums [32mPASSED[0m[32m              [ 63%][0m
tests/test_api.py::test_api_estimated_status [32mPASSED[0m[32m                      [ 72%][0m
tests/test_api.py::test_setup_checks [32mPASSED[0m[32m                              [ 81%][0m
tests/test_bill.py::test_allocate_bill_exact_match [32mPASSED[0m[32m                [ 90%][0m
tests/test_classify.py::test_flow_classification [32mPASSED[0m[32m                  [100%][0m

[32m============================== [32m[1m11 passed[0m[32m in 1.22s[0m[32m ==============================[0m
## 2. Docker Compose Build and Up
 Image flowtab-backend Building 
 Image flowtab-frontend Building 
#1 [internal] load local bake definitions
#1 reading from stdin 1.02kB done
#1 DONE 0.0s

#2 [frontend internal] load build definition from Dockerfile
#2 transferring dockerfile: 157B done
#2 DONE 0.0s

#3 [backend internal] load build definition from Dockerfile
#3 transferring dockerfile: 232B done
#3 DONE 0.0s

#4 [backend internal] load metadata for docker.io/library/python:3.12-slim
#4 DONE 0.0s

#5 [backend internal] load .dockerignore
#5 transferring context: 96B done
#5 DONE 0.0s

#6 [backend 1/5] FROM docker.io/library/python:3.12-slim
#6 DONE 0.0s

#7 [backend internal] load build context
#7 transferring context: 327.79kB 0.0s done
#7 DONE 0.0s

#8 [backend 2/5] WORKDIR /app
#8 CACHED

#9 [backend 3/5] COPY requirements.txt .
#9 CACHED

#10 [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt
#10 CACHED

#11 [backend 5/5] COPY . .
#11 DONE 0.1s

#12 [frontend internal] load metadata for docker.io/library/node:20-alpine
#12 DONE 0.4s

#13 [backend] exporting to image
#13 exporting layers 0.0s done
#13 writing image sha256:b7dba7fe0cf3c381be59e5d8d32c9df28c8472d414275e95809de6c30da3f2c6 done
#13 naming to docker.io/library/flowtab-backend done
#13 DONE 0.0s

#14 [backend] resolving provenance for metadata file
#14 DONE 0.0s

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

#19 [frontend 2/5] WORKDIR /app
#19 CACHED

#20 [frontend 4/5] RUN npm ci
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
time="2026-10-06T09:01:16+05:30" level=warning msg="No services to build"
 Network flowtab_default Creating 
 Network flowtab_default Created 
 Volume flowtab_postgres_data Creating 
 Volume flowtab_postgres_data Created 
 Container flowtab-db-1 Creating 
 Container flowtab-db-1 Created 
 Container flowtab-db-1 Starting 
 Container flowtab-db-1 Started 
time="2026-10-06T09:01:21+05:30" level=warning msg="No services to build"
 Container flowtab-db-1 Running 
 Container flowtab-backend-1 Creating 
 Container flowtab-backend-1 Created 
 Container flowtab-frontend-1 Creating 
 Container flowtab-frontend-1 Created 
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
{"status":"success","total_gb":75011.34,"total_usd":3864.39,"by_category":{"NAT Gateway Data Processing":2268.06,"Inter-AZ Data Transfer":84.1,"Inter-Region Data Transfer":33.6,"Internet Egress":1478.64},"daily_series":[{"date":"2026-09-29","gb":7862.7,"usd":348.303,"hourly":[{"hour":"2026-09-29T03:00:00","gb":371.66,"usd":16.4918},{"hour":"2026-09-29T04:00:00","gb":371.84,"usd":16.4354},{"hour":"2026-09-29T05:00:00","gb":378.04,"usd":16.7582},{"hour":"2026-09-29T06:00:00","gb":368.99,"usd":16.3798},{"hour":"2026-09-29T07:00:00","gb":378.29,"usd":16.7523},{"hour":"2026-09-29T08:00:00","gb":375.24,"usd":16.609},{"hour":"2026-09-29T09:00:00","gb":374.02,"usd":16.5387},{"hour":"2026-09-29T10:00:00","gb":373.98,"usd":16.6132},{"hour":"2026-09-29T11:00:00","gb":369.72,"usd":16.43},{"hour":"2026-09-29T12:00:00","gb":375.78,"usd":16.597},{"hour":"2026-09-29T13:00:00","gb":377.64,"usd":16.6867},{"hour":"2026-09-29T14:00:00","gb":377.06,"usd":16.6985},{"hour":"2026-09-29T15:00:00","gb":371.72,"usd":16.4559},{"hour":"2026-09-29T16:00:00","gb":377.76,"usd":16.7239},{"hour":"2026-09-29T17:00:00","gb":371.22,"usd":16.4966},{"hour":"2026-09-29T18:00:00","gb":374.57,"usd":16.6103},{"hour":"2026-09-29T19:00:00","gb":376.07,"usd":16.6383},{"hour":"2026-09-29T20:00:00","gb":379.6,"usd":16.7857},{"hour":"2026-09-29T21:00:00","gb":374.17,"usd":16.5903},{"hour":"2026-09-29T22:00:00","gb":372.97,"usd":16.4933},{"hour":"2026-09-29T23:00:00","gb":372.37,"usd":16.518}]},{"date":"2026-09-30","gb":8987.0,"usd":398.1347,"hourly":[{"hour":"2026-09-30T00:00:00","gb":370.33,"usd":16.4265},{"hour":"2026-09-30T01:00:00","gb":376.46,"usd":16.682},{"hour":"2026-09-30T02:00:00","gb":371.4,"usd":16.4368},{"hour":"2026-09-30T03:00:00","gb":377.59,"usd":16.6575},{"hour":"2026-09-30T04:00:00","gb":374.48,"usd":16.6418},{"hour":"2026-09-30T05:00:00","gb":370.76,"usd":16.4812},{"hour":"2026-09-30T06:00:00","gb":381.51,"usd":16.8343},{"hour":"2026-09-30T07:00:00","gb":377.0,"usd":16.6698},{"hour":"2026-09-30T08:00:00","gb":375.01,"usd":16.6655},{"hour":"2026-09-30T09:00:00","gb":371.55,"usd":16.4621},{"hour":"2026-09-30T10:00:00","gb":380.37,"usd":16.7944},{"hour":"2026-09-30T11:00:00","gb":371.05,"usd":16.4814},{"hour":"2026-09-30T12:00:00","gb":372.35,"usd":16.5159},{"hour":"2026-09-30T13:00:00","gb":371.79,"usd":16.4064},{"hour":"2026-09-30T14:00:00","gb":369.46,"usd":16.4234},{"hour":"2026-09-30T15:00:00","gb":374.85,"usd":16.5668},{"hour":"2026-09-30T16:00:00","gb":378.71,"usd":16.7708},{"hour":"2026-09-30T17:00:00","gb":378.31,"usd":16.7859},{"hour":"2026-09-30T18:00:00","gb":376.67,"usd":16.6834},{"hour":"2026-09-30T19:00:00","gb":369.38,"usd":16.3965},{"hour":"2026-09-30T20:00:00","gb":370.23,"usd":16.4354},{"hour":"2026-09-30T21:00:00","gb":378.81,"usd":16.7637},{"hour":"2026-09-30T22:00:00","gb":372.54,"usd":16.4431},{"hour":"2026-09-30T23:00:00","gb":376.39,"usd":16.71}]},{"date":"2026-10-01","gb":8986.54,"usd":398.016,"hourly":[{"hour":"2026-10-01T00:00:00","gb":376.57,"usd":16.685},{"hour":"2026-10-01T01:00:00","gb":378.37,"usd":16.7192},{"hour":"2026-10-01T02:00:00","gb":370.49,"usd":16.4172},{"hour":"2026-10-01T03:00:00","gb":376.61,"usd":16.6511},{"hour":"2026-10-01T04:00:00","gb":371.84,"usd":16.4179},{"hour":"2026-10-01T05:00:00","gb":370.79,"usd":16.4284},{"hour":"2026-10-01T06:00:00","gb":370.8,"usd":16.4528},{"hour":"2026-10-01T07:00:00","gb":373.89,"usd":16.5539},{"hour":"2026-10-01T08:00:00","gb":379.55,"usd":16.7683},{"hour":"2026-10-01T09:00:00","gb":375.27,"usd":16.5741},{"hour":"2026-10-01T10:00:00","gb":374.61,"usd":16.5951},{"hour":"2026-10-01T11:00:00","gb":369.75,"usd":16.3914},{"hour":"2026-10-01T12:00:00","gb":377.76,"usd":16.7413},{"hour":"2026-10-01T13:00:00","gb":380.57,"usd":16.8306},{"hour":"2026-10-01T14:00:00","gb":369.81,"usd":16.4054},{"hour":"2026-10-01T15:00:00","gb":374.04,"usd":16.5618},{"hour":"2026-10-01T16:00:00","gb":375.22,"usd":16.6826},{"hour":"2026-10-01T17:00:00","gb":374.97,"usd":16.6572},{"hour":"2026-10-01T18:00:00","gb":371.12,"usd":16.423},{"hour":"2026-10-01T19:00:00","gb":375.32,"usd":16.6118},{"hour":"2026-10-01T20:00:00","gb":372.57,"usd":16.4981},{"hour":"2026-10-01T21:00:00","gb":378.6,"usd":16.7426},{"hour":"2026-10-01T22:00:00","gb":374.54,"usd":16.6045},{"hour":"2026-10-01T23:00:00","gb":373.49,"usd":16.6026}]},{"date":"2026-10-02","gb":9008.07,"usd":398.8293,"hourly":[{"hour":"2026-10-02T00:00:00","gb":381.82,"usd":16.848},{"hour":"2026-10-02T01:00:00","gb":377.35,"usd":16.7495},{"hour":"2026-10-02T02:00:00","gb":379.26,"usd":16.7489},{"hour":"2026-10-02T03:00:00","gb":373.0,"usd":16.5388},{"hour":"2026-10-02T04:00:00","gb":375.45,"usd":16.6023},{"hour":"2026-10-02T05:00:00","gb":378.68,"usd":16.7537},{"hour":"2026-10-02T06:00:00","gb":374.75,"usd":16.592},{"hour":"2026-10-02T07:00:00","gb":375.51,"usd":16.6189},{"hour":"2026-10-02T08:00:00","gb":376.82,"usd":16.6944},{"hour":"2026-10-02T09:00:00","gb":372.49,"usd":16.5291},{"hour":"2026-10-02T10:00:00","gb":375.1,"usd":16.5772},{"hour":"2026-10-02T11:00:00","gb":372.01,"usd":16.4425},{"hour":"2026-10-02T12:00:00","gb":377.75,"usd":16.8031},{"hour":"2026-10-02T13:00:00","gb":373.8,"usd":16.5502},{"hour":"2026-10-02T14:00:00","gb":375.93,"usd":16.7019},{"hour":"2026-10-02T15:00:00","gb":369.74,"usd":16.401},{"hour":"2026-10-02T16:00:00","gb":375.04,"usd":16.5566},{"hour":"2026-10-02T17:00:00","gb":377.25,"usd":16.7676},{"hour":"2026-10-02T18:00:00","gb":375.18,"usd":16.5677},{"hour":"2026-10-02T19:00:00","gb":374.77,"usd":16.5469},{"hour":"2026-10-02T20:00:00","gb":371.82,"usd":16.4074},{"hour":"2026-10-02T21:00:00","gb":372.31,"usd":16.5223},{"hour":"2026-10-02T22:00:00","gb":375.92,"usd":16.6001},{"hour":"2026-10-02T23:00:00","gb":376.32,"usd":16.7092}]},{"date":"2026-10-03","gb":9017.69,"usd":399.6111,"hourly":[{"hour":"2026-10-03T00:00:00","gb":374.75,"usd":16.6377},{"hour":"2026-10-03T01:00:00","gb":376.87,"usd":16.7377},{"hour":"2026-10-03T02:00:00","gb":376.77,"usd":16.6394},{"hour":"2026-10-03T03:00:00","gb":375.26,"usd":16.6174},{"hour":"2026-10-03T04:00:00","gb":375.64,"usd":16.5736},{"hour":"2026-10-03T05:00:00","gb":377.78,"usd":16.7685},{"hour":"2026-10-03T06:00:00","gb":378.17,"usd":16.7626},{"hour":"2026-10-03T07:00:00","gb":375.3,"usd":16.6226},{"hour":"2026-10-03T08:00:00","gb":371.33,"usd":16.4797},{"hour":"2026-10-03T09:00:00","gb":377.52,"usd":16.7001},{"hour":"2026-10-03T10:00:00","gb":376.85,"usd":16.6452},{"hour":"2026-10-03T11:00:00","gb":378.83,"usd":16.7961},{"hour":"2026-10-03T12:00:00","gb":378.12,"usd":16.8032},{"hour":"2026-10-03T13:00:00","gb":381.44,"usd":16.839},{"hour":"2026-10-03T14:00:00","gb":372.82,"usd":16.5403},{"hour":"2026-10-03T15:00:00","gb":373.15,"usd":16.5573},{"hour":"2026-10-03T16:00:00","gb":376.48,"usd":16.6822},{"hour":"2026-10-03T17:00:00","gb":378.11,"usd":16.8087},{"hour":"2026-10-03T18:00:00","gb":372.35,"usd":16.4561},{"hour":"2026-10-03T19:00:00","gb":375.49,"usd":16.6748},{"hour":"2026-10-03T20:00:00","gb":368.39,"usd":16.373},{"hour":"2026-10-03T21:00:00","gb":379.56,"usd":16.7886},{"hour":"2026-10-03T22:00:00","gb":374.95,"usd":16.6445},{"hour":"2026-10-03T23:00:00","gb":371.77,"usd":16.463}]},{"date":"2026-10-04","gb":19495.77,"usd":1343.4853,"hourly":[{"hour":"2026-10-04T00:00:00","gb":379.59,"usd":16.7687},{"hour":"2026-10-04T01:00:00","gb":373.03,"usd":16.4799},{"hour":"2026-10-04T02:00:00","gb":377.95,"usd":16.6886},{"hour":"2026-10-04T03:00:00","gb":876.21,"usd":61.6585},{"hour":"2026-10-04T04:00:00","gb":873.49,"usd":61.5462},{"hour":"2026-10-04T05:00:00","gb":876.64,"usd":61.6813},{"hour":"2026-10-04T06:00:00","gb":871.61,"usd":61.4895},{"hour":"2026-10-04T07:00:00","gb":877.45,"usd":61.7511},{"hour":"2026-10-04T08:00:00","gb":875.25,"usd":61.6162},{"hour":"2026-10-04T09:00:00","gb":869.48,"usd":61.3999},{"hour":"2026-10-04T10:00:00","gb":873.6,"usd":61.5189},{"hour":"2026-10-04T11:00:00","gb":873.89,"usd":61.5736},{"hour":"2026-10-04T12:00:00","gb":875.83,"usd":61.66},{"hour":"2026-10-04T13:00:00","gb":876.46,"usd":61.6492},{"hour":"2026-10-04T14:00:00","gb":874.93,"usd":61.6283},{"hour":"2026-10-04T15:00:00","gb":875.9,"usd":61.6902},{"hour":"2026-10-04T16:00:00","gb":874.62,"usd":61.6026},{"hour":"2026-10-04T17:00:00","gb":872.22,"usd":61.552},{"hour":"2026-10-04T18:00:00","gb":876.42,"usd":61.6799},{"hour":"2026-10-04T19:00:00","gb":873.72,"usd":61.5699},{"hour":"2026-10-04T20:00:00","gb":874.15,"usd":61.5969},{"hour":"2026-10-04T21:00:00","gb":876.84,"usd":61.6472},{"hour":"2026-10-04T22:00:00","gb":874.49,"usd":61.582},{"hour":"2026-10-04T23:00:00","gb":872.0,"usd":61.4547}]},{"date":"2026-10-05","gb":10526.83,"usd":531.2679,"hourly":[{"hour":"2026-10-05T00:00:00","gb":873.62,"usd":61.5132},{"hour":"2026-10-05T01:00:00","gb":872.41,"usd":61.5427},{"hour":"2026-10-05T02:00:00","gb":875.18,"usd":61.5952},{"hour":"2026-10-05T03:00:00","gb":375.67,"usd":16.6129},{"hour":"2026-10-05T04:00:00","gb":378.34,"usd":16.7165},{"hour":"2026-10-05T05:00:00","gb":379.69,"usd":16.7577},{"hour":"2026-10-05T06:00:00","gb":373.37,"usd":16.5195},{"hour":"2026-10-05T07:00:00","gb":379.5,"usd":16.775},{"hour":"2026-10-05T08:00:00","gb":372.61,"usd":16.5214},{"hour":"2026-10-05T09:00:00","gb":372.76,"usd":16.4611},{"hour":"2026-10-05T10:00:00","gb":375.71,"usd":16.698},{"hour":"2026-10-05T11:00:00","gb":379.16,"usd":16.7518},{"hour":"2026-10-05T12:00:00","gb":372.57,"usd":16.5104},{"hour":"2026-10-05T13:00:00","gb":379.01,"usd":16.7937},{"hour":"2026-10-05T14:00:00","gb":376.48,"usd":16.6281},{"hour":"2026-10-05T15:00:00","gb":375.87,"usd":16.5966},{"hour":"2026-10-05T16:00:00","gb":379.37,"usd":16.8245},{"hour":"2026-10-05T17:00:00","gb":375.52,"usd":16.5849},{"hour":"2026-10-05T18:00:00","gb":373.58,"usd":16.5869},{"hour":"2026-10-05T19:00:00","gb":376.55,"usd":16.7029},{"hour":"2026-10-05T20:00:00","gb":380.9,"usd":16.8134},{"hour":"2026-10-05T21:00:00","gb":371.22,"usd":15.3492},{"hour":"2026-10-05T22:00:00","gb":380.99,"usd":15.7833},{"hour":"2026-10-05T23:00:00","gb":376.73,"usd":15.6289}]},{"date":"2026-10-06","gb":1126.75,"usd":46.7474,"hourly":[{"hour":"2026-10-06T00:00:00","gb":371.54,"usd":15.4515},{"hour":"2026-10-06T01:00:00","gb":375.65,"usd":15.5526},{"hour":"2026-10-06T02:00:00","gb":379.55,"usd":15.7434}]}]}
```

### GET /api/v1/network/charges
```json
{"status":"success","data":[{"charge_category":"NAT Gateway Data Processing","gb":50401.3,"usd":2268.0586,"share_of_total":0.5869,"flow_count":168},{"charge_category":"Inter-AZ Data Transfer","gb":8410.04,"usd":84.1004,"share_of_total":0.0218,"flow_count":168},{"charge_category":"Inter-Region Data Transfer","gb":1680.0,"usd":33.6,"share_of_total":0.0087,"flow_count":168},{"charge_category":"Internet Egress","gb":14520.0,"usd":1478.6357,"share_of_total":0.3826,"flow_count":192}]}
```

### GET /api/v1/network/flow-graph
```json
{"status":"success","data":{"nodes":[{"id":"POD:workers-pod-3","label":"workers-pod-3","type":"POD"},{"id":"POD:auth-pod-1","label":"auth-pod-1","type":"POD"},{"id":"POD:reports-pod-4","label":"reports-pod-4","type":"POD"},{"id":"INTERNET:S3 via NAT","label":"S3 via NAT","type":"INTERNET"},{"id":"POD:gateway-pod-0","label":"gateway-pod-0","type":"POD"},{"id":"EC2:RDS Master","label":"RDS Master","type":"EC2"},{"id":"EC2:RDS Replica","label":"RDS Replica","type":"EC2"},{"id":"ELB:Public ALB","label":"Public ALB","type":"ELB"},{"id":"INTERNET:Unknown IP","label":"Unknown IP","type":"INTERNET"},{"id":"INTERNET:Public Web","label":"Public Web","type":"INTERNET"}],"links":[{"source":"POD:reports-pod-4","target":"INTERNET:S3 via NAT","route":"nat-egress","usd":2268.0586},{"source":"POD:gateway-pod-0","target":"POD:auth-pod-1","route":"cross-az","usd":84.1004},{"source":"EC2:RDS Master","target":"EC2:RDS Replica","route":"cross-region","usd":33.6},{"source":"ELB:Public ALB","target":"INTERNET:Public Web","route":"elb-egress","usd":398.6357},{"source":"POD:workers-pod-3","target":"INTERNET:Unknown IP","route":"internet-egress","usd":1080.0}]}}
```

### GET /api/v1/network/architecture
```json
{"status":"success","data":{"accounts":[{"account_id":"111111111111","regions":[{"region":"us-east-2","vpcs":[{"vpc_id":"vpc-a1","name":"Prod EKS","resources":[{"eni_id":"eni-nat","resource_type":"NAT","resource_id":"nat-123","name":"NAT Gateway","private_ip":"10.0.1.5"},{"eni_id":"eni-alb","resource_type":"ELB","resource_id":"alb-pub","name":"Public ALB","private_ip":"10.0.1.6"}]},{"vpc_id":"vpc-a2","name":"Prod Data","resources":[{"eni_id":"eni-rds-us","resource_type":"RDS","resource_id":"rds-master","name":"RDS Master","private_ip":"10.0.2.10"}]}]}]},{"account_id":"222222222222","regions":[{"region":"ap-south-1","vpcs":[{"vpc_id":"vpc-b1","name":"DR Data","resources":[{"eni_id":"eni-rds-ap","resource_type":"RDS","resource_id":"rds-replica","name":"RDS Replica","private_ip":"10.0.3.10"}]}]}]}]}}
```

### GET /api/v1/network/reconciliation
```json
{"status":"success","data":[{"charge_category":"NAT Gateway Data Processing","estimated_usd":2186.8632,"billed_usd":2186.8632,"waiting_for_bill_usd":81.1954,"difference_usd":0.0,"difference_percent":0.0,"status":"matched"},{"charge_category":"Inter-AZ Data Transfer","estimated_usd":81.0869,"billed_usd":81.0869,"waiting_for_bill_usd":3.0134,"difference_usd":0.0,"difference_percent":0.0,"status":"matched"},{"charge_category":"Inter-Region Data Transfer","estimated_usd":32.4,"billed_usd":32.4,"waiting_for_bill_usd":1.2,"difference_usd":0.0,"difference_percent":0.0,"status":"matched"},{"charge_category":"Internet Egress","estimated_usd":1298.7,"billed_usd":1470.5357,"waiting_for_bill_usd":8.1,"difference_usd":171.8357,"difference_percent":13.23,"status":"corrected"}]}
```

### GET /api/v1/network/coverage
```json
{"status":"success","data":{"vpcs_covered":3,"total_vpcs":3}}
```

### GET /api/v1/network/findings
```json
{"status":"success","findings":[{"title":"S3 Traffic via NAT Gateway","description":"Large volume of traffic routing to S3 via NAT Gateway. Consider adding an S3 Gateway Endpoint to the VPC to eliminate these costs.","severity":"high","cost_impact":2268.06},{"title":"High Inter-AZ Communication","description":"Significant costs from chatty pods across AZs (e.g. gateway to auth). Co-locating frequent communicators can reduce this.","severity":"medium","cost_impact":84.1},{"title":"Cross-Region Database Replication","description":"Consistent outbound data transfer across regions detected. Verify this is authorized replication.","severity":"low","cost_impact":33.6},{"title":"Spike in Internet Egress (2026-10-04)","description":"Egress out of ALB spiked over 3x the running average of $56.41/day.","severity":"high","cost_impact":946.45},{"title":"Spike in Internet Egress (2026-10-05)","description":"Egress out of ALB spiked over 3x the running average of $56.41/day.","severity":"high","cost_impact":133.26},{"title":"ALB True-Outbound Correction","description":"Flow logs undercount application layer bytes inside ALB connections. Bill reconciliation corrected a massive ~44% difference.","severity":"medium","cost_impact":163.74}]}
```

### GET /api/v1/network/setup/checks
```json
{"status":"success","data":{"flow_logs":true,"cur":true,"mode":"demo"}}
```

### GET /api/v1/network/flows
```json
{"status":"success","data":[{"sender_type":"POD","sender_name":"reports-pod-4","receiver_type":"INTERNET","receiver_name":"S3 via NAT","route":"nat-egress","charge_category":"NAT Gateway Data Processing","gb":50401.3,"usd":2268.0586},{"sender_type":"POD","sender_name":"gateway-pod-0","receiver_type":"POD","receiver_name":"auth-pod-1","route":"cross-az","charge_category":"Inter-AZ Data Transfer","gb":8410.04,"usd":84.1004},{"sender_type":"EC2","sender_name":"RDS Master","receiver_type":"EC2","receiver_name":"RDS Replica","route":"cross-region","charge_category":"Inter-Region Data Transfer","gb":1680.0,"usd":33.6},{"sender_type":"ELB","sender_name":"Public ALB","receiver_type":"INTERNET","receiver_name":"Public Web","route":"elb-egress","charge_category":"Internet Egress","gb":2520.0,"usd":398.6357},{"sender_type":"POD","sender_name":"workers-pod-3","receiver_type":"INTERNET","receiver_name":"Unknown IP","route":"internet-egress","charge_category":"Internet Egress","gb":12000.0,"usd":1080.0}]}
```
