locals {
  common_tags = {
    "TF_Workspace" = var.tf_workspace
    "Terraform"    = "true"
  }
}

module "registration_infra" {
  source  = "app.terraform.io/OKTKD/tkd-registration/kseppler"
  version = "~>0.1.0"

  processing_queue_name           = var.processing_queue_name
  failed_registrations_queue_name = var.failed_registrations_queue_name
  registration_table_name         = var.registration_table_name
  profile_pics_bucket_name        = var.profile_pics_bucket_name
  badges_bucket_name              = var.badges_bucket_name
  config_bucket_name              = var.config_bucket_name
  public_media_bucket_name        = var.public_media_bucket_name
  profile_pics_bucket_prefix      = var.profile_pics_bucket_prefix
  badges_bucket_prefix            = var.badges_bucket_prefix
  config_bucket_prefix            = var.config_bucket_prefix
  public_media_bucket_prefix      = var.public_media_bucket_prefix
  domain_name                     = var.domain_name
  common_tags                     = local.common_tags
}

resource "aws_s3_object" "backend_json" {
  bucket = module.registration_infra.config_bucket_name
  key    = "backend.json"
  content = jsonencode(tomap({
    EMAIL_SERVER       = var.email_send_server
    EMAIL_PORT         = var.email_send_port
    EMAIL_PASSWD       = var.email_send_password
    FROM_EMAIL         = var.email_send_address
    ADMIN_EMAIL        = var.admin_email
    STRIPE_API_KEY     = var.stripe_api_key
    COMPETITION_NAME   = var.competition_name
    COMPETITION_YEAR   = var.competition_year
    CONTACT_EMAIL      = var.contact_email
    PROFILE_PIC_BUCKET = module.registration_infra.profile_pics_bucket_name
    BADGE_BUCKET       = module.registration_infra.badges_bucket_name
    CONFIG_BUCKET      = module.registration_infra.config_bucket_name
    SQS_QUEUE_URL      = module.registration_infra.processing_queue_url
    DB_TABLE           = var.registration_table_name
  }))
  content_type           = "application/json"
  server_side_encryption = "AES256"
  storage_class          = "STANDARD"
  tags                   = local.common_tags
}

resource "aws_s3_object" "frontend_json" {
  bucket = module.registration_infra.config_bucket_name
  key    = "frontend.json"
  content = jsonencode(tomap({
    MAPS_API_KEY        = var.maps_api_key
    STRIPE_API_KEY      = var.stripe_api_key
    REG_URL             = "https://${var.domain_name}"
    COMPETITION_NAME    = var.competition_name
    COMPETITION_YEAR    = var.competition_year
    EARLY_REG_DATE      = var.early_reg_date
    REG_CLOSE_DATE      = var.reg_close_date
    CONTACT_EMAIL       = var.contact_email
    PROFILE_PIC_BUCKET  = module.registration_infra.profile_pics_bucket_name
    CONFIG_BUCKET       = module.registration_infra.config_bucket_name
    PUBLIC_MEDIA_BUCKET = module.registration_infra.public_media_bucket_name
    SQS_QUEUE_URL       = module.registration_infra.processing_queue_url
    DB_TABLE            = var.registration_table_name
    VISITOR_INFO_URL    = var.visitor_info_url
    VISITOR_INFO_TEXT   = var.visitor_info_text
  }))
  content_type           = "application/json"
  server_side_encryption = "AES256"
  storage_class          = "STANDARD"
  tags                   = local.common_tags
}
