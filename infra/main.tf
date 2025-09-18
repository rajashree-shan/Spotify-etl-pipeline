provider "aws" {
  region=var.region
}
resource "aws_s3_bucket" "spotify" {bucket=var.bucket_name}
resource "aws_iam_role" "lambda_role" {name="spotify-lambda-role" assume_role_policy=data.aws_iam_policy_document.lambda_assume_role.json}
data "aws_iam_policy_document" "lambda_assume_role" {statement {actions=["sts:AssumeRole"] principals {type="Service" identifiers=["lambda.amazonaws.com"]}}}
resource "aws_iam_role_policy" "lambda_policy" {role=aws_iam_role.lambda_role.id policy=data.aws_iam_policy_document.lambda_policy_doc.json}
data "aws_iam_policy_document" "lambda_policy_doc" {statement {actions=["s3:GetObject","s3:PutObject","s3:ListBucket"] resources=["${aws_s3_bucket.spotify.arn}","${aws_s3_bucket.spotify.arn}/*"]} statement {actions=["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"] resources=["*"]}}
resource "aws_lambda_function" "spotify_lambda" {filename="lambda_transform.zip" function_name="spotify-transform" role=aws_iam_role.lambda_role.arn handler="lambda_handler.handler" runtime="python3.10" environment {variables={S3_BUCKET=var.bucket_name}}}
resource "aws_s3_bucket_notification" "bucket_notify" {bucket=aws_s3_bucket.spotify.id lambda_function {lambda_function_arn=aws_lambda_function.spotify_lambda.arn events=["s3:ObjectCreated:*"] filter_prefix="raw/spotify/"}}
resource "aws_lambda_permission" "allow_s3" {statement_id="AllowS3Invoke" action="lambda:InvokeFunction" function_name=aws_lambda_function.spotify_lambda.function_name principal="s3.amazonaws.com" source_arn=aws_s3_bucket.spotify.arn}
