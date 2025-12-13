/**
 * Observability Module
 * 
 * Sets up monitoring, logging, and alerting infrastructure
 * - Prometheus for metrics collection
 * - Grafana for visualization
 * - CloudWatch for AWS-native monitoring
 */

# Prometheus Configuration
resource "aws_instance" "prometheus" {
  count = var.enable_prometheus ? 1 : 0
  
  ami           = var.prometheus_ami_id
  instance_type = var.prometheus_instance_type
  subnet_id     = var.subnet_ids[0]
  
  tags = {
    Name        = "${var.environment}-prometheus"
    Environment = var.environment
    Service     = "monitoring"
  }
  
  user_data = <<-EOF
              #!/bin/bash
              # Install Prometheus
              # PLACEHOLDER: Add Prometheus installation script
              EOF
}

# Grafana Configuration
resource "aws_instance" "grafana" {
  count = var.enable_grafana ? 1 : 0
  
  ami           = var.grafana_ami_id
  instance_type = var.grafana_instance_type
  subnet_id     = var.subnet_ids[0]
  
  tags = {
    Name        = "${var.environment}-grafana"
    Environment = var.environment
    Service     = "visualization"
  }
  
  user_data = <<-EOF
              #!/bin/bash
              # Install Grafana
              # PLACEHOLDER: Add Grafana installation script
              # Admin password: ${var.grafana_admin_password}
              EOF
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "application" {
  name              = "/aws/application/${var.environment}/expense-app"
  retention_in_days = var.log_retention_days
  
  tags = {
    Environment = var.environment
    Service     = "logging"
  }
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "${var.environment}-high-cpu-usage"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors EC2 CPU utilization"
  alarm_actions       = var.alarm_actions
  
  tags = {
    Environment = var.environment
  }
}

# SNS Topic for Alerts
resource "aws_sns_topic" "alerts" {
  name = "${var.environment}-monitoring-alerts"
  
  tags = {
    Environment = var.environment
    Service     = "alerting"
  }
}

resource "aws_sns_topic_subscription" "email_alerts" {
  count = var.alert_email != "" ? 1 : 0
  
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# Prometheus Data Storage (EBS Volume)
resource "aws_ebs_volume" "prometheus_data" {
  count = var.enable_prometheus ? 1 : 0
  
  availability_zone = data.aws_subnet.selected[0].availability_zone
  size              = var.prometheus_storage_size
  type              = "gp3"
  encrypted         = true
  
  tags = {
    Name        = "${var.environment}-prometheus-data"
    Environment = var.environment
  }
}

data "aws_subnet" "selected" {
  count = length(var.subnet_ids) > 0 ? 1 : 0
  id    = var.subnet_ids[0]
}

# Placeholder for Alertmanager
# Uncomment to enable Alertmanager for Prometheus
# resource "aws_instance" "alertmanager" {
#   count = var.enable_alertmanager ? 1 : 0
#   
#   ami           = var.alertmanager_ami_id
#   instance_type = "t3.micro"
#   subnet_id     = var.subnet_ids[0]
#   
#   tags = {
#     Name        = "${var.environment}-alertmanager"
#     Environment = var.environment
#   }
# }
