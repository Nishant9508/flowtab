# flowtab

An AWS data transfer cost visibility tool that points to exactly where your transfer cost comes from (which resource sends data, where it goes, and why it's charged), with totals guaranteed to reconcile against your AWS bill (CUR).

## Architecture
- **Backend:** Python FastAPI, analyzing flow logs (S3 Parquet via Athena) combined with inventory snapshots.
- **Frontend:** React + TypeScript.
- **Database:** PostgreSQL.
- **Deployment:** Docker Compose (local/demo), Helm & Terraform (customer install).
