variable "environment" {
  description = "Environment name"
  type        = string
}

variable "secrets" {
  description = "Map of secret names to secret identifiers"
  type        = map(string)
}

variable "enable_rotation" {
  description = "Enable automatic secret rotation"
  type        = bool
  default     = false
}

variable "rotation_lambda_arn" {
  description = "ARN of Lambda function for secret rotation"
  type        = string
  default     = ""
}

# Uncomment when using Azure Key Vault
# variable "azure_key_vault_id" {
#   description = "Azure Key Vault ID"
#   type        = string
#   default     = ""
# }
