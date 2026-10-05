# Manual Validation With Real AWS

By default, flowtab operates in synthetic demo mode `DEMO_MODE=false`. To run manually against your AWS account:

1. **Deploy Terraform module:**
   Navigate to `deploy/terraform/` and run:
   ```bash
   terraform init && terraform apply -var="flowtab_account_id=YOUR_ACCOUNT" -var="cur_bucket_name=YOUR_BUCKET"
   ```

2. **Supply AWS Credentials:**
   Locally configure environment variables, or rely on `~/.aws/credentials`:
   ```bash
   export AWS_PROFILE=read-only-admin
   export DEMO_MODE=false
   docker compose up backend
   ```

3. **Verify via API:**
   ```bash
   curl localhost:8000/api/v1/network/summary
   ```
   If valid AWS credentials exist, you will receive real metadata analysis.
