# Flowtab Audit against PLAN.md

| Milestone | Task | Status | File / Component | Test / Screenshot |
|---|---|---|---|---|
| M1 Demo Mode | Design DB schema | Done | `backend/app/models.py` | `tests/test_api.py`, `tests/test_bill.py` |
| M1 Demo Mode | Create generator | Done | `backend/tests/generator/demo_data.py` | `tests/test_api.py::test_generate_demo` |
| M1 Demo Mode | Expose API endpoint `/api/v1/demo/generate` | Done | `backend/app/api/demo.py` | `tests/test_api.py::test_generate_demo` |
| M1 Demo Mode | Update frontend to render | Missing | `frontend/src/components/Dashboard.tsx` | No test, no screenshot |
| M2 Data Pipeline | Map required IAM permissions | Missing | `backend/app/network/collect.py` | No passing test |
| M2 Data Pipeline | Create generic SQL abstraction for Athena | Missing | `backend/app/network/athena.py` | No passing test |
| M2 Data Pipeline | Inventory collection snapshotter | Missing | `backend/app/network/collect.py` | No passing test |
| M2 Data Pipeline | Routing/charge-type classifier logic | Done | `backend/app/network/classify.py` | `tests/test_classify.py` |
| M2 Data Pipeline | Unit tests for classifier | Done | `tests/test_classify.py` | `tests/test_classify.py` |
| M3 Pricing | Integrate AWS Price List API parsing | Missing | `backend/app/network/bill.py` | No passing test |
| M3 Pricing | Build CUR 2.0 parser & processor | Missing | `backend/app/network/bill.py` | No passing test |
| M3 Pricing | Implement bill-first allocation algorithm | Done | `backend/app/network/bill.py` | `tests/test_bill.py::test_allocate_bill_exact_match` |
| M3 Pricing | Implement 'waiting for bill' state | Done | `backend/app/network/bill.py` | `tests/test_bill.py::test_allocate_bill_exact_match` |
| M4 Multi-account | Implement AWS Organizations scoped scanning | Missing | `backend/app/api/network/scopes.py` | No passing test |
| M4 Multi-account | Manage scope enablement through config | Missing | `backend/app/api/network/scopes.py` | No passing test |
| M4 Multi-account | Add aggregate endpoints mapping cross-account coverage | Missing | `backend/app/api/network/scopes.py` | No passing test |
| M5 Product UI | Build high-level reporting views | Missing | `frontend/src/components/Dashboard.tsx` | No test, no screenshot |
| M5 Product UI | Interactive filtering mechanism | Missing | `frontend/src/components/Dashboard.tsx` | No test, no screenshot |
| M5 Product UI | Component architecture diagram | Missing | `frontend/src/components/Dashboard.tsx` | No test, no screenshot |
| M5 Product UI | "Setup" probe interface | Missing | `frontend/src/components/Setup.tsx` | No test, no screenshot |
| M5 Product UI | Data Table with CSV export | Missing | `frontend/src/components/Dashboard.tsx` | No test, no screenshot |
| M6 Findings & Alerts | Configurable rules engine | Missing | `backend/app/network/alerts.py` | No passing test |
| M6 Findings & Alerts | Text generation module | Missing | `backend/app/network/alerts.py` | No passing test |
| M6 Findings & Alerts | Slack integration framework | Missing | N/A | No passing test |
| M7 Security | Implement robust auth middleware | Missing | `backend/app/auth.py` | No passing test |
| M7 Security | Integrate local user authentication + open OIDC stub | Missing | `backend/app/auth.py` | No passing test |
| M7 Security | Write docs/SECURITY.md | Missing | `docs/SECURITY.md` | No passing test |
| M7 Security | Wire up database audit logging | Missing | N/A | No passing test |
| M8 Packaging | Build deploy/terraform/ module | Missing | `deploy/terraform/main.tf` | No passing test |
| M8 Packaging | Build Dockerfile and standard Helm Chart | Missing | `deploy/helm/flowtab/Chart.yaml` | No passing test |
| M8 Packaging | Draft installation pipeline script/guide | Missing | N/A | No passing test |
| M9 Docs & Assets | Take screenshots from the demo mode | Missing | N/A | No passing test / screenshot |
| M9 Docs & Assets | Create clean, professional README.md | Missing | `README.md` | No passing test |
| M9 Docs & Assets | docs/BUSINESS.md | Missing | `docs/BUSINESS.md` | No passing test |
| M9 Docs & Assets | docs/MANUAL_VALIDATION.md | Missing | `docs/MANUAL_VALIDATION.md` | No passing test |
