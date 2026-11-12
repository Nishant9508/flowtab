# Flowtab

**Find out why your AWS data transfer bill is high.**

AWS bills data transfer as a handful of usage types and never tells you which
resource sent the data or where it went. Flowtab joins your VPC flow logs with
your Cost and Usage Report (CUR) so you can see who is sending data to whom,
what it costs, and what to change, with totals that reconcile to your bill.

## What it does

- Attributes data transfer cost to pods, load balancers, instances and
  gateways, not just usage types
- Classifies every flow by charge type: internet egress, cross-region,
  cross-AZ, NAT gateway, transit gateway, PrivateLink and more
- Reconciles estimates against the bill and corrects under-counted flows
  (flow logs can miss a large share of load balancer traffic)
- Surfaces findings in plain language, such as "this pod sends 50 TB to S3
  through a NAT gateway; a free S3 gateway endpoint would remove that cost"
- Runs self-hosted in your account, so your network data never leaves it
