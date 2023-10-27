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

resource "aws_acm_certificate" "main" {
  provider = aws.us-east-1

  domain_name               = var.domain_name
  key_algorithm             = "RSA_2048"
  subject_alternative_names = [var.domain_name]
  validation_method         = "DNS"
  options {
    certificate_transparency_logging_preference = "ENABLED"
  }
}

resource "aws_route53_record" "validation" {
  for_each = {
    for dvo in aws_acm_certificate.main.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = module.registration_infra.domain_zone_id
}

resource "aws_acm_certificate_validation" "main" {
  provider = aws.us-east-1

  certificate_arn         = aws_acm_certificate.main.arn
  validation_record_fqdns = [for record in aws_route53_record.validation : record.fqdn]
}