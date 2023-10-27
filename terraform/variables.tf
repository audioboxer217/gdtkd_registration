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

variable "domain_name" {
  type        = string
  description = "The domain to use for this site."
}
