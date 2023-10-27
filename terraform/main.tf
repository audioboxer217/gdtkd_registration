module "registration_infra" {
  source  = "app.terraform.io/OKTKD/tkd-registration/kseppler"
  version = "~>0.0.2"

  processing_queue_name           = var.processing_queue_name
  failed_registrations_queue_name = var.failed_registrations_queue_name
  registration_table_name         = var.registration_table_name
  profile_pics_bucket_name        = var.profile_pics_bucket_name
  badges_bucket_name              = var.badges_bucket_name
  config_bucket_name              = var.config_bucket_name
  profile_pics_bucket_prefix      = var.profile_pics_bucket_prefix
  badges_bucket_prefix            = var.badges_bucket_prefix
  config_bucket_prefix            = var.config_bucket_prefix
  domain_name                     = var.domain_name
}
