/**
 * Secrets Management Module
 * 
 * Manages secrets using AWS Secrets Manager and HashiCorp Vault placeholders
 */

# AWS Secrets Manager
resource "aws_secretsmanager_secret" "app_secrets" {
  for_each = var.secrets
  
  name        = "${var.environment}-${each.value}"
  description = "Secret for ${each.key} in ${var.environment}"
  
  recovery_window_in_days = var.environment == "production" ? 30 : 7
  
  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_secretsmanager_secret_version" "app_secrets" {
  for_each = var.secrets
  
  secret_id     = aws_secretsmanager_secret.app_secrets[each.key].id
  secret_string = jsonencode({
    value = "PLACEHOLDER_${upper(each.key)}_VALUE"
  })
  
  lifecycle {
    ignore_changes = [secret_string]
  }
}

# Rotation configuration
resource "aws_secretsmanager_secret_rotation" "app_secrets" {
  for_each = var.enable_rotation ? var.secrets : {}
  
  secret_id           = aws_secretsmanager_secret.app_secrets[each.key].id
  rotation_lambda_arn = var.rotation_lambda_arn
  
  rotation_rules {
    automatically_after_days = 30
  }
}

# HashiCorp Vault Configuration (Placeholder)
# Uncomment and configure when using Vault
# resource "vault_generic_secret" "app_secrets" {
#   for_each = var.secrets
#   
#   path = "${var.environment}/expense-app/${each.key}"
#   
#   data_json = jsonencode({
#     value = "PLACEHOLDER_${upper(each.key)}_VALUE"
#   })
# }

# Azure Key Vault Configuration (Placeholder)
# Uncomment and configure when using Azure
# resource "azurerm_key_vault_secret" "app_secrets" {
#   for_each = var.secrets
#   
#   name         = replace(each.key, "_", "-")
#   value        = "PLACEHOLDER_${upper(each.key)}_VALUE"
#   key_vault_id = var.azure_key_vault_id
# }
