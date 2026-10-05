# Project Status

## Milestones

- [x] **M0 Foundation**: repo layout, config via environment, Docker Compose, CI, test setup, banned-strings check, README skeleton.
- [x] **M1 Synthetic demo mode**: generator for fake accounts, VPCs, EKS pods, flow logs and fully hand-computable costs.
- [x] **M2 Data pipeline**: flow log integration via Athena (abstracted), read-only inventory snapshots (EC2, ELB, EKS, RDS, ElastiCache, etc.), classifier for route and charge type.
- [x] **M3 Pricing and bill reconciliation**: Price List API fallback, CUR 2.0 reconciliation (`line_item_resource_id`), bill-first allocation, waiting-for-bill state logic.
- [x] **M4 Multi-account/region**: AWS Organizations discovery, scopes configuration, coverage view per-account.
- [x] **M5 Product UI**: summary, filtering by charge type, multi-level flow architecture diagram (account > region > VPC > AZ/subnet), bill comparison, setup probes.
- [x] **M6 Findings and alerts**: plain-language cause explanation, weekly Slack summary, spike alerts.
- [x] **M7 Security**: OIDC/SSO, local admin login, role-based access, audit logging, least-privilege IAM policy.
- [x] **M8 Packaging**: Terraform module for read-only roles/CUR, CloudFormation, Docker image, Helm chart, versioned releases, launch telemetry framework.
- [x] **M9 Docs and launch assets**: Architecture diagram, manual validation guide, business/pricing docs, and a static landing page built from demo screenshots.
