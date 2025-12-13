/**
 * Development Environment - Variables
 */

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "development"
}

# Networking Variables
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "public_subnets" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnets" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.11.0/24", "10.0.12.0/24"]
}

# Compute Variables
variable "backend_instance_type" {
  description = "EC2 instance type for backend"
  type        = string
  default     = "t3.micro"
}

variable "backend_desired_capacity" {
  description = "Desired number of backend instances"
  type        = number
  default     = 1
}

# Database Variables
variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Allocated storage for database (GB)"
  type        = number
  default     = 20
}

variable "database_name" {
  description = "Name of the database"
  type        = string
  default     = "expense_app_dev"
}

# Observability Variables
variable "grafana_admin_password" {
  description = "Admin password for Grafana (use secrets manager in production)"
  type        = string
  sensitive   = true
  default     = "changeme"
}
