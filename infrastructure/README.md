# Infrastructure as Code

This directory contains Infrastructure as Code (IaC) definitions for deploying and managing the Expense Settlement Application.

## Directory Structure

```
infrastructure/
├── terraform/           # Terraform IaC definitions
│   ├── environments/   # Environment-specific configurations
│   │   ├── dev/       # Development environment
│   │   └── prod/      # Production environment
│   ├── modules/       # Reusable Terraform modules
│   │   ├── networking/    # VPC, subnets, security groups
│   │   ├── compute/       # EC2, ECS, or other compute resources
│   │   ├── database/      # RDS or database configuration
│   │   ├── secrets/       # Secrets management setup
│   │   └── observability/ # Monitoring and logging
├── ci-cd/              # CI/CD pipeline configurations
└── docs/               # Infrastructure documentation
```

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- Cloud provider CLI (AWS CLI, Azure CLI, or GCP SDK)
- Appropriate cloud credentials configured

## Quick Start

### Development Environment

```bash
cd infrastructure/terraform/environments/dev
terraform init
terraform plan
terraform apply
```

### Production Environment

```bash
cd infrastructure/terraform/environments/prod
terraform init
terraform plan
terraform apply
```

## Secrets Management

Secrets are managed using:
- **AWS Secrets Manager** (for AWS deployments)
- **HashiCorp Vault** (for multi-cloud or on-premise)
- **Azure Key Vault** (for Azure deployments)

Never commit secrets to version control. Use environment variables or secret management tools.

## Observability

The infrastructure includes setup for:
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization and dashboards
- **CloudWatch/Application Insights**: Cloud-native monitoring
- Logging aggregation and analysis

## Best Practices

1. **State Management**: Use remote state storage (S3, Azure Storage, or Terraform Cloud)
2. **Modules**: Keep modules reusable and well-documented
3. **Versioning**: Pin provider and module versions
4. **Security**: Follow least-privilege principle for IAM/RBAC
5. **Cost Optimization**: Use appropriate instance sizes and auto-scaling
6. **Disaster Recovery**: Implement backup and recovery procedures

## CI/CD Integration

Infrastructure changes should be deployed through CI/CD pipelines. See `ci-cd/` directory for pipeline configurations.

## Support

For infrastructure-related questions or issues, consult the documentation in `docs/` or contact the DevOps team.
