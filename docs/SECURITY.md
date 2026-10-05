# flowtab Security Architecture

flowtab is designed with a strictly read-only, bill-first approach. 

## 1. Authentication & Authorization
- **OIDC/SSO:** The dashboard requires an active OIDC session to view reports or trigger checks.
- **Role-based Access:** By default all users have read-only access. Only explicit admins can manage organizational scopes or manually trigger synchronization.

## 2. Infrastructure Access (AWS)
- flowtab uses **Read-Only IAM Roles**.
- We never request `cloudtrail:*` mutation, `iam:Create*`, or `ec2:Run*` privileges.
- We require read-only Athena access to your Cost & Usage Report (CUR) bucket.
- No outbound network connections are required for core functionality. 

## 3. Data Processing
- Flow records are aggregated to the hour before they land in our DB.
- Raw payload data is explicitly dropping (VPC flow logs don't capture payload, only headers).
- Banned company-specific strings are strictly checked in our CI.

## 4. Audit Logging
- Every API route modification is logged locally for compliance.
