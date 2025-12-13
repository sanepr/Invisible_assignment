output "prometheus_endpoint" {
  description = "Prometheus server endpoint"
  value       = var.enable_prometheus && length(aws_instance.prometheus) > 0 ? "http://${aws_instance.prometheus[0].private_ip}:9090" : ""
}

output "grafana_endpoint" {
  description = "Grafana dashboard URL"
  value       = var.enable_grafana && length(aws_instance.grafana) > 0 ? "http://${aws_instance.grafana[0].private_ip}:3000" : ""
}

output "alertmanager_endpoint" {
  description = "Alertmanager endpoint"
  value       = "" # PLACEHOLDER: Uncomment when alertmanager is enabled
}

output "cloudwatch_log_group_name" {
  description = "CloudWatch log group name"
  value       = aws_cloudwatch_log_group.application.name
}

output "sns_topic_arn" {
  description = "SNS topic ARN for alerts"
  value       = aws_sns_topic.alerts.arn
}
