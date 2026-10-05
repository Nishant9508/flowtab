variable "flowtab_account_id" {
  type        = string
  description = "The AWS account ID where the flowtab instances run (e.g. your centralized tooling account)"
}

variable "cur_bucket_name" {
  type        = string
  description = "The S3 bucket holding the CUR 2.0 exports"
}

# 1. Provide read-only access to AWS Inventory
resource "aws_iam_role" "flowtab_readonly" {
  name = "flowtab-readonly-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { AWS = "arn:aws:iam::${var.flowtab_account_id}:root" }
    }]
  })
}

resource "aws_iam_role_policy" "flowtab_readonly_policy" {
  name = "flowtab-inventory-read"
  role = aws_iam_role.flowtab_readonly.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:DescribeInstances",
          "ec2:DescribeNatGateways",
          "ec2:DescribeNetworkInterfaces",
          "elasticloadbalancing:DescribeLoadBalancers",
          "rds:DescribeDBInstances"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:s3:::${var.cur_bucket_name}",
          "arn:aws:s3:::${var.cur_bucket_name}/*"
        ]
      }
    ]
  })
}
