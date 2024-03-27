# General Inputs
variable "tf_workspace" {
  type        = string
  description = "The name of the Workspace in Terraform Cloud that manages this deployment"
}

variable "application_name" {
  type        = string
  description = "The name to use for the AWS Appication"
}

# Competition Details
variable "domain_name" {
  type        = string
  description = "The domain to use for this site."
}

variable "email_send_server" {
  type        = string
  description = "The email server to send emails from."
}

variable "email_send_port" {
  type        = string
  description = "The port for the email server to send emails from."
}

variable "email_send_address" {
  type        = string
  description = "The email address to use to send emails from."
}

variable "email_send_password" {
  type        = string
  sensitive   = true
  description = "The password for the 'email_send_address'."
}

variable "competition_name" {
  type        = string
  description = "The name of the competition."
}

variable "competition_year" {
  type        = string
  description = "The year of the competition."
}

variable "contact_email" {
  type        = string
  description = "The email to give to users as a contact."
}

# API Details
variable "maps_api_key" {
  type        = string
  sensitive   = true
  description = "The API Key for Google Maps."
}

variable "stripe_api_key" {
  type        = string
  sensitive   = true
  description = "The API Key for Stripe."
}

# AWS Resource Inputs
variable "processing_queue_name" {
  type        = string
  description = "The name to use for the 'processing' SQS Queue."
  default     = "processing"
}

variable "failed_registrations_queue_name" {
  type        = string
  description = "The name to use for the 'failed' SQS Queue."
  default     = "failed_registrations"
}

variable "registration_table_name" {
  type        = string
  description = "The name to use for 'registrations' DynamoDB Table."
}

variable "profile_pics_bucket_name" {
  type        = string
  description = "The name to use for bucket that will hold the Profile Pics (Overrides `profile_pics_bucket_prefix` if provided)."
  default     = ""
}

variable "badges_bucket_name" {
  type        = string
  description = "The name to use for bucket that will hold the Badges (Overrides `badges_bucket_prefix` if provided)."
  default     = ""
}

variable "config_bucket_name" {
  type        = string
  description = "The name to use for bucket that will hold the Configs (Overrides `config_bucket_prefix` if provided)."
  default     = ""
}

variable "public_media_bucket_name" {
  type        = string
  description = "The name to use for bucket that will hold the public media (Overrides `public_media_bucket_prefix` if provided)."
  default     = ""
}

variable "profile_pics_bucket_prefix" {
  type        = string
  description = "The prefix to use for bucket that will hold the Profile Pics."
  default     = "tkd-reg-profile-pics"
}

variable "badges_bucket_prefix" {
  type        = string
  description = "The prefix to use for bucket that will hold the Badges."
  default     = "tkd-reg-badges"
}

variable "config_bucket_prefix" {
  type        = string
  description = "The prefix to use for bucket that will hold the Configs."
  default     = "tkd-reg-config"
}

variable "public_media_bucket_prefix" {
  type        = string
  description = "The prefix to use for bucket that will hold the public media."
  default     = "tkd-reg-public-media"
}
