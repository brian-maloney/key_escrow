resource "aws_s3_bucket" "key_escrow" {
  bucket = "vond-key-escrow"
}

resource "aws_s3_bucket_ownership_controls" "key_escrow" {
  bucket = aws_s3_bucket.key_escrow.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "key_escrow" {
  bucket = aws_s3_bucket.key_escrow.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}
