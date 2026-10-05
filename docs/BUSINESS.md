# Flowtab Business & Pricing Logic

flowtab strictly adheres to the AWS Pricing strategy for data transfer:

## Cross-AZ Data Transfer
- AWS charges $0.01 per GB in each direction ($0.02 total).
- flowtab models this as `Inter-AZ Data Transfer` catching `cross-az` flows between internal subnets of the same VPC.
- The allocator checks for identical Region but differing AZ IDs on source and destination.

## Egress to Internet
- Public egress via ELB, NAT Gateway, or directly mapped EC2 EIP is tracked as `Internet Egress`.
- AWS bills tier-based pricing (starting at $0.09/GB for first 10TB).
- flowtab automatically digests the effective rate directly from your CUR, bypassing tiered manual math. 

## NAT Gateway
- Processing charges ($0.045/GB) are explicitly separated from the standard Internet Egress that happens alongside it, isolating 'preventable' costs.
