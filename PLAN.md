# Flowtab Implementation Plan

## Goal
Build a standalone, installable AWS data transfer cost analysis tool ("flowtab") that relies on the customer's CUR (bill-first allocation) and augmenting VPC flow logs. It must run securely in customer environments, requiring no outbound connectivity except optional telemetry. Every step must be free of restricted/banned identifiers from the old prototype.

## Milestones & Tasks

### M0 Foundation (Repo Layout & CI)
- [ ] Create `check-banned-strings.sh` pre-commit/CI script.
- [ ] Setup repository structure (`backend/`, `frontend/`, `docs/`, `deploy/`).
- [ ] Initialize Python FastAPI backend (`requirements.txt`, `pytest` configuration, `ruff` for linting).
- [ ] Initialize React + TS frontend framework (Vite, `vitest`, TailwindCSS).
- [ ] Define initial local development environment (`docker-compose.yml` for DB, Backend, Frontend).
- [ ] Create basic CI pipeline (`.github/workflows/ci.yml`) to run DB setup, string checks, python tests, and typescript linting/tests.

*(Acceptance: `docker compose up` brings up empty scaffold. CI passes. Committing a file with a banned word fails the hook.)*

### M1 Synthetic Demo Mode (Standalone Logic)
- [ ] Design DB schema in `backend/app/models.py` (Snapshots, Resources, Flow logs, Billed lines).
- [ ] Create `backend/tests/generator/` to synthesize predictable infrastructure (VPCs, AZs, NAT Gateways, ELBs, Pods).
- [ ] Generate fake but mathematically rigid flow log entries matched exactly to fake CUR billing lines.
- [ ] Expose an API endpoint `/api/v1/demo/generate` alongside standard reads so the UI can work purely against this data.
- [ ] Update frontend to render this structural mockup.

*(Acceptance: UI renders data from synthetic mode successfully. Tests can run against this generator without any AWS credentials.)*

### M2 Data pipeline (Collection & Classification)
- [ ] Map required IAM permissions & read-only logic without external libraries where boto3 simple calls suffice.
- [ ] Create generic SQL abstraction for Athena (S3 Parquet queries).
- [ ] Inventory collection snapshotter (using simple read-only API tokens rather than requiring heavy tools).
- [ ] Routing/charge-type classifier logic (NAT, Transit Gateway, cross-AZ, Peerings, Egress).
- [ ] Unit tests for the classifier against explicit data scenarios (using demo generator data).

*(Acceptance: Flow log processor correctly maps flows to source and destination identities based purely on captured inventory and metadata.)*

### M3 Pricing and Bill Reconciliation
- [ ] Integrate AWS Price List API parsing (caching rates).
- [ ] Build CUR 2.0 parser & processor (reconcile by `line_item_resource_id` with tag fallback).
- [ ] Implement bill-first allocation algorithm: taking the exact exact CUR cost and dividing it proportionately amongst candidate flows.
- [ ] Implement 'waiting for bill' state (pricing strictly from Price List API when CUR is not yet available).

*(Acceptance: All demo/test flows properly allocate 100% of the simulated bill exactly, down to the cent.)*

### M4 Multi-account/region & Discovery
- [ ] Implement AWS Organizations scoped scanning (AssumeRole chaining) across configured scopes.
- [ ] Manage scope enablement through database / local config.
- [ ] Add aggregate endpoints mapping cross-account coverage per region and VPC.

*(Acceptance: Backend safely processes configured scopes ignoring unreachable items but reporting them in the coverage view.)*

### M5 Product UI
- [ ] Build high-level reporting views (Monthly summaries, Top flows).
- [ ] Interactive filtering mechanism per charge type.
- [ ] Component architecture diagram mapping nested resources (Account > Region > VPC > Subnet/AZ).
- [ ] "Setup" probe interface that issues dry AWS calls to report readiness (flow logs active, permissions valid).
- [ ] Data Table with CSV export capabilities.

*(Acceptance: A user can visually navigate from an Organization-level transfer sum down to an individual Pod talking to the Internet.)*

### M6 Findings and Alerts
- [ ] Configurable rules engine for common data-transfer antipatterns (e.g. Cross-AZ chat, missing S3 endpoints).
- [ ] Text generation module for clear plain-text recommendations.
- [ ] Slack integration framework for weekly rollup delivery.

*(Acceptance: System generates actionable alerts on the synthetic demo data (e.g., detecting our fake Cross-AZ chatter test scenario).)*

### M7 Security
- [ ] Implement robust auth middleware.
- [ ] Integrate local user authentication + open OIDC stub.
- [ ] Write `docs/SECURITY.md`.
- [ ] Wire up database audit logging (API access).

*(Acceptance: All previously open API endpoints require a valid token. No credentials logged. Customer facing security doc is clean.)*

### M8 Packaging
- [ ] Build `deploy/terraform/` module matching the required read-only capabilities and flow log S3 vending.
- [ ] Build Dockerfile and standard Helm Chart configuration.
- [ ] Draft an installation pipeline script/guide in `<30 minutes`.

*(Acceptance: Helm chart installs clean onto a mock cluster. Terraform plan completes successfully against isolated dummy state.)*

### M9 Docs & Launch Assets
- [ ] Take screenshots from the demo mode.
- [ ] Create clean, professional `README.md`.
- [ ] `docs/BUSINESS.md` for logic transparency mapping charges back to Amazon's exact pricing terminology.
- [ ] `docs/MANUAL_VALIDATION.md` for how to test manually.

*(Acceptance: Repository is fully self-contained, branded "flowtab", clean of old company traces, and ready to ship.)*
