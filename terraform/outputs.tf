output "processing_queue_url" {
  description = "The URL for the Processing SQS Queue."
  value       = module.registration_infra.processing_queue_url
}

output "config_bucket_name" {
  description = "The name of the Config S3 Bucket."
  value       = module.registration_infra.config_bucket_name
}

output "profile_pics_bucket_name" {
  description = "The name of the Profile Pics S3 Bucket."
  value       = module.registration_infra.profile_pics_bucket_name
}

output "badges_bucket_name" {
  description = "The name of the Badges S3 Bucket."
  value       = module.registration_infra.badges_bucket_name
}

output "domain_name_servers" {
  description = "The list of name servers for the domain."
  value       = module.registration_infra.domain_name_servers
}

output "certificate_arn" {
  description = "The ARN for the domain certificate"
  value       = aws_acm_certificate.main.arn
}
