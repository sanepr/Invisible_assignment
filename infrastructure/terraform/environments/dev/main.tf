/**
 * Development Environment - Main Configuration
 * 
 * This file defines the infrastructure for the development environment.
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
  # Uncomment and configure for remote state
  # backend "s3" {
  #   bucket         = "your-terraform-state-bucket"
  #   key            = "expense-app/dev/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "terraform-state-lock"
  # }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = "development"
      Project     = "expense-settlement-app"
      ManagedBy   = "terraform"
    }
  }
}

# Networking Module
module "networking" {
  source = "../../modules/networking"
  
  environment         = var.environment
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  public_subnets     = var.public_subnets
  private_subnets    = var.private_subnets
}

# Compute Module (Backend API)
module "compute" {
  source = "../../modules/compute"
  
  environment    = var.environment
  vpc_id         = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
  instance_type  = var.backend_instance_type
  desired_capacity = var.backend_desired_capacity
}

# Database Module
module "database" {
  source = "../../modules/database"
  
  environment        = var.environment
  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
  instance_class     = var.db_instance_class
  allocated_storage  = var.db_allocated_storage
  database_name      = var.database_name
}

# Secrets Management Module
module "secrets" {
  source = "../../modules/secrets"
  
  environment = var.environment
  secrets = {
    jwt_secret_key     = "expense-app-jwt-secret-dev"
    database_password  = "expense-app-db-password-dev"
    api_keys          = "expense-app-api-keys-dev"
  }
}

# Observability Module
module "observability" {
  source = "../../modules/observability"
  
  environment = var.environment
  vpc_id      = module.networking.vpc_id
  subnet_ids  = module.networking.private_subnet_ids
  
  # Prometheus configuration
  enable_prometheus = true
  prometheus_retention_days = 15
  
  # Grafana configuration
  enable_grafana = true
  grafana_admin_password = var.grafana_admin_password
}
