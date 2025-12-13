/**
 * Production Environment - Main Configuration
 * 
 * This file defines the infrastructure for the production environment.
 * Production has higher availability, scalability, and security requirements.
 */

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Backend configuration for state storage
  # REQUIRED for production - use remote state
  # backend "s3" {
  #   bucket         = "your-terraform-state-bucket-prod"
  #   key            = "expense-app/prod/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "terraform-state-lock"
  # }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = "production"
      Project     = "expense-settlement-app"
      ManagedBy   = "terraform"
      CostCenter  = "engineering"
    }
  }
}

# Networking Module - Multi-AZ for high availability
module "networking" {
  source = "../../modules/networking"
  
  environment         = var.environment
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  public_subnets     = var.public_subnets
  private_subnets    = var.private_subnets
}

# Compute Module (Backend API) - Auto-scaling enabled
module "compute" {
  source = "../../modules/compute"
  
  environment        = var.environment
  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
  instance_type      = var.backend_instance_type
  desired_capacity   = var.backend_desired_capacity
  min_capacity       = var.backend_min_capacity
  max_capacity       = var.backend_max_capacity
}

# Database Module - Multi-AZ with read replicas
module "database" {
  source = "../../modules/database"
  
  environment        = var.environment
  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
  instance_class     = var.db_instance_class
  allocated_storage  = var.db_allocated_storage
  database_name      = var.database_name
  multi_az           = true
  backup_retention_period = 30
  enable_read_replica = true
}

# Secrets Management Module
module "secrets" {
  source = "../../modules/secrets"
  
  environment = var.environment
  secrets = {
    jwt_secret_key     = "expense-app-jwt-secret-prod"
    database_password  = "expense-app-db-password-prod"
    api_keys          = "expense-app-api-keys-prod"
  }
  
  # Enable automatic rotation for production
  enable_rotation = true
}

# Observability Module - Enhanced monitoring
module "observability" {
  source = "../../modules/observability"
  
  environment = var.environment
  vpc_id      = module.networking.vpc_id
  subnet_ids  = module.networking.private_subnet_ids
  
  # Prometheus configuration
  enable_prometheus = true
  prometheus_retention_days = 90
  prometheus_high_availability = true
  
  # Grafana configuration
  enable_grafana = true
  grafana_admin_password = var.grafana_admin_password
  
  # Alerting configuration
  enable_alertmanager = true
  alert_email = var.alert_email
  alert_slack_webhook = var.alert_slack_webhook
}
