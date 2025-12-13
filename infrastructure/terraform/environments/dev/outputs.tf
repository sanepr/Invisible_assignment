/**
 * Development Environment - Outputs
 */

output "vpc_id" {
  description = "VPC ID"
  value       = module.networking.vpc_id
}

output "backend_endpoint" {
  description = "Backend API endpoint"
  value       = module.compute.endpoint
}

output "database_endpoint" {
  description = "Database endpoint"
  value       = module.database.endpoint
  sensitive   = true
}

output "prometheus_endpoint" {
  description = "Prometheus endpoint"
  value       = module.observability.prometheus_endpoint
}

output "grafana_endpoint" {
  description = "Grafana dashboard URL"
  value       = module.observability.grafana_endpoint
}

output "secrets_arns" {
  description = "ARNs of created secrets"
  value       = module.secrets.secret_arns
  sensitive   = true
}
