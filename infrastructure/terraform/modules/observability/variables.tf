variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
}

# Prometheus Variables
variable "enable_prometheus" {
  description = "Enable Prometheus deployment"
  type        = bool
  default     = true
}

variable "prometheus_instance_type" {
  description = "Instance type for Prometheus"
  type        = string
  default     = "t3.small"
}

variable "prometheus_ami_id" {
  description = "AMI ID for Prometheus instance"
  type        = string
  default     = "ami-xxxxxxxxx" # PLACEHOLDER: Update with actual AMI
}

variable "prometheus_retention_days" {
  description = "Prometheus data retention in days"
  type        = number
  default     = 15
}

variable "prometheus_storage_size" {
  description = "Prometheus storage size in GB"
  type        = number
  default     = 50
}

variable "prometheus_high_availability" {
  description = "Enable Prometheus HA setup"
  type        = bool
  default     = false
}

# Grafana Variables
variable "enable_grafana" {
  description = "Enable Grafana deployment"
  type        = bool
  default     = true
}

variable "grafana_instance_type" {
  description = "Instance type for Grafana"
  type        = string
  default     = "t3.small"
}

variable "grafana_ami_id" {
  description = "AMI ID for Grafana instance"
  type        = string
  default     = "ami-xxxxxxxxx" # PLACEHOLDER: Update with actual AMI
}

variable "grafana_admin_password" {
  description = "Admin password for Grafana"
  type        = string
  sensitive   = true
}

# CloudWatch Variables
variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30
}

variable "alarm_actions" {
  description = "SNS topic ARNs for alarm actions"
  type        = list(string)
  default     = []
}

# Alerting Variables
variable "enable_alertmanager" {
  description = "Enable Alertmanager for Prometheus"
  type        = bool
  default     = false
}

variable "alert_email" {
  description = "Email address for alerts"
  type        = string
  default     = ""
}

variable "alert_slack_webhook" {
  description = "Slack webhook URL for alerts"
  type        = string
  sensitive   = true
  default     = ""
}

variable "alertmanager_ami_id" {
  description = "AMI ID for Alertmanager instance"
  type        = string
  default     = "ami-xxxxxxxxx" # PLACEHOLDER: Update with actual AMI
}
