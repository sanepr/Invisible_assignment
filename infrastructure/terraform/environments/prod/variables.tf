/**
 * Production Environment - Variables
 */

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

# Networking Variables
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.1.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones (3 for production HA)"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "public_subnets" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.1.1.0/24", "10.1.2.0/24", "10.1.3.0/24"]
}

variable "private_subnets" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.1.11.0/24", "10.1.12.0/24", "10.1.13.0/24"]
}

# Compute Variables - Production sizing
variable "backend_instance_type" {
  description = "EC2 instance type for backend"
  type        = string
  default     = "t3.medium"
}

variable "backend_desired_capacity" {
  description = "Desired number of backend instances"
  type        = number
  default     = 3
}

variable "backend_min_capacity" {
  description = "Minimum number of backend instances"
  type        = number
  default     = 2
}

variable "backend_max_capacity" {
  description = "Maximum number of backend instances"
  type        = number
  default     = 10
}

# Database Variables - Production sizing
variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.medium"
}

variable "db_allocated_storage" {
  description = "Allocated storage for database (GB)"
  type        = number
  default     = 100
}

variable "database_name" {
  description = "Name of the database"
  type        = string
  default     = "expense_app_prod"
}

# Observability Variables
variable "grafana_admin_password" {
  description = "Admin password for Grafana (use secrets manager)"
  type        = string
  sensitive   = true
}

variable "alert_email" {
  description = "Email for critical alerts"
  type        = string
  default     = "devops@example.com"
}

variable "alert_slack_webhook" {
  description = "Slack webhook URL for alerts"
  type        = string
  sensitive   = true
  default     = ""
}
