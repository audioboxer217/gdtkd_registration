import {
  to = module.registration_infra.aws_sqs_queue.processing_queue
  id = "https://sqs.us-east-2.amazonaws.com/799879571353/processing"
}

import {
  to = module.registration_infra.aws_sqs_queue.failed_registrations_queue
  id = "https://sqs.us-east-2.amazonaws.com/799879571353/failed_registrations"
}

import {
  to = module.registration_infra.aws_s3_bucket.config_bucket
  id = "gdtkd-reg-config"
}

import {
  to = module.registration_infra.aws_s3_bucket.badges_bucket
  id = "gdtkd-reg-badges"
}

import {
  to = module.registration_infra.aws_s3_bucket.profile-pics_bucket
  id = "gdtkd-reg-profile-pics"
}

import {
  to = module.registration_infra.aws_dynamodb_table.registrations_table
  id = "okgp_2024_registration"
}

import {
  to = module.registration_infra.aws_route53_zone.main
  id = "Z09376522CF3PU6SHG99X"
}

import {
  to = aws_acm_certificate.main
  id = "arn:aws:acm:us-east-1:799879571353:certificate/8893e1e9-4a35-43a3-a547-eed14e496a50"
}

import {
  to = aws_route53_record.validation["okgp24.kseppler.com"]
  id = "Z09376522CF3PU6SHG99X__cce5bd29df9e9acc0e67a9d0a98105c5.okgp24.kseppler.com._CNAME"
}
