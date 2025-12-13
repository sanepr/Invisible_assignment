# Infrastructure Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Terraform** (>= 1.0)
   ```bash
   # macOS
   brew install terraform
   
   # Linux
   wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
   unzip terraform_1.6.0_linux_amd64.zip
   sudo mv terraform /usr/local/bin/
   ```

2. **AWS CLI** (for AWS deployments)
   ```bash
   # macOS
   brew install awscli
   
   # Linux
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   ```

3. **Cloud Provider Credentials**
   - AWS: Configure with `aws configure`
   - Azure: `az login`
   - GCP: `gcloud auth login`

## Initial Setup

### 1. Configure Backend State Storage

For production use, configure remote state storage:

**AWS S3 Backend:**
```bash
# Create S3 bucket for state
aws s3 mb s3://your-terraform-state-bucket --region us-east-1

# Create DynamoDB table for state locking
aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --region us-east-1
```

Update `backend` configuration in `main.tf`:
```hcl
backend "s3" {
  bucket         = "your-terraform-state-bucket"
  key            = "expense-app/dev/terraform.tfstate"
  region         = "us-east-1"
  encrypt        = true
  dynamodb_table = "terraform-state-lock"
}
```

### 2. Set Environment Variables

Create a `.envrc` file (use with direnv):
```bash
export AWS_REGION=us-east-1
export TF_VAR_grafana_admin_password="your-secure-password"
export TF_VAR_alert_email="devops@example.com"
```

### 3. Initialize Terraform

```bash
cd infrastructure/terraform/environments/dev
terraform init
```

## Deployment

### Development Environment

```bash
cd infrastructure/terraform/environments/dev

# Review planned changes
terraform plan

# Apply changes
terraform apply

# View outputs
terraform output
```

### Production Environment

```bash
cd infrastructure/terraform/environments/prod

# Review planned changes
terraform plan

# Apply changes (requires confirmation)
terraform apply

# View outputs
terraform output
```

## Module Development

When creating new modules:

1. Place module in `infrastructure/terraform/modules/<module-name>/`
2. Include `main.tf`, `variables.tf`, and `outputs.tf`
3. Document module purpose and variables in a `README.md`
4. Test module in dev environment first

## Secrets Management

### AWS Secrets Manager

Store secrets securely:
```bash
# Create a secret
aws secretsmanager create-secret \
  --name dev-expense-app-jwt-secret \
  --secret-string "your-jwt-secret-key"

# Update a secret
aws secretsmanager update-secret \
  --secret-id dev-expense-app-jwt-secret \
  --secret-string "new-secret-value"

# Retrieve a secret
aws secretsmanager get-secret-value \
  --secret-id dev-expense-app-jwt-secret
```

### HashiCorp Vault (Optional)

If using Vault:
```bash
# Enable KV secrets engine
vault secrets enable -path=expense-app kv-v2

# Store a secret
vault kv put expense-app/dev/jwt-secret value="your-secret"

# Retrieve a secret
vault kv get expense-app/dev/jwt-secret
```

## Monitoring Setup

### Prometheus

After deployment, access Prometheus at the endpoint from outputs:
```bash
terraform output prometheus_endpoint
```

Configure scrape targets in `/etc/prometheus/prometheus.yml`

### Grafana

Access Grafana at the endpoint from outputs:
```bash
terraform output grafana_endpoint
```

Default credentials:
- Username: `admin`
- Password: (from `grafana_admin_password` variable)

Import dashboards from the Grafana dashboard library.

## Troubleshooting

### State Lock Issues

If state is locked:
```bash
# Force unlock (use with caution)
terraform force-unlock <lock-id>
```

### Module Not Found

Ensure modules are initialized:
```bash
terraform get -update
```

### Authentication Errors

Verify cloud credentials are configured:
```bash
# AWS
aws sts get-caller-identity

# Azure
az account show

# GCP
gcloud auth list
```

## Cleanup

To destroy infrastructure:

**Development:**
```bash
cd infrastructure/terraform/environments/dev
terraform destroy
```

**Production (use with extreme caution):**
```bash
cd infrastructure/terraform/environments/prod
terraform destroy
```

## Next Steps

1. Customize module implementations for your cloud provider
2. Configure CI/CD pipelines (see `ci-cd/` directory)
3. Set up monitoring dashboards in Grafana
4. Configure alerting rules in Prometheus/Alertmanager
5. Implement backup and disaster recovery procedures

## Support

For questions or issues:
- Review documentation in `infrastructure/docs/`
- Check Terraform documentation: https://www.terraform.io/docs
- Contact DevOps team
