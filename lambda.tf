module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 4.7.2"

  function_name              = "key-escrow"
  create_function            = true
  create_lambda_function_url = true
  handler                    = "key_escrow.lambda_handler"
  architectures              = ["arm64"]
  timeout                    = 300

  compatible_runtimes = ["python3.9"]
  runtime             = "python3.9"

  attach_policy_statements = true
  policy_statements = {
    s3_read = {
      effect    = "Allow",
      actions   = ["s3:HeadObject", "s3:GetObject"],
      resources = ["${aws_s3_bucket.key_escrow.arn}/*"]
    }
  }

  cloudwatch_logs_retention_in_days = 90

  source_path = [
    {
      path = "${path.module}/lambda/",
    },
    {
      pip_requirements = "${path.module}/lambda/requirements.txt",
    }
  ]
}

output "function_url" {
  value = module.lambda.lambda_function_url
}
