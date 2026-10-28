# AWS Serverless Log Analyzer

A small event-driven cloud project: uploading a `.log` file to an Amazon S3 `logs/` prefix triggers an AWS Lambda function. The function counts INFO, WARNING, ERROR and DEBUG lines, then saves a JSON report under `reports/`.

## Architecture

`Upload log -> Amazon S3 (logs/) -> S3 ObjectCreated event -> AWS Lambda (Python) -> JSON report in S3 (reports/) -> CloudWatch Logs`

## Services and concepts demonstrated

- Amazon S3 object storage and event notifications
- AWS Lambda serverless compute and event-driven processing
- IAM execution-role permissions and least privilege
- Amazon CloudWatch Logs for troubleshooting
- JSON output and Python text processing

## Files

- `lambda_function.py`: Lambda handler
- `sample.log`: test input
- `sample_expected_report.json`: illustrative expected result for the sample file

## Build steps (AWS Console)

1. Choose one AWS Region and use it for S3, Lambda and CloudWatch.
2. Create a general-purpose S3 bucket with a globally unique name. Keep Block Public Access enabled and do not make the bucket public.
3. Create an IAM execution role for Lambda. Attach the AWS managed `AWSLambdaBasicExecutionRole` policy for CloudWatch logging. Add a custom policy restricted to your bucket and prefixes:
   - `s3:GetObject` on `arn:aws:s3:::YOUR_BUCKET_NAME/logs/*`
   - `s3:PutObject` on `arn:aws:s3:::YOUR_BUCKET_NAME/reports/*`
4. Create a Lambda function named `serverless-log-analyzer`, runtime Python 3.x available in your console, and select the role created above.
5. Paste `lambda_function.py` into the Lambda code editor and choose Deploy.
6. Add an S3 trigger to the Lambda function. Select your bucket, event type `All object create events`, and set the prefix filter to `logs/`. This prefix is important: output reports are written to `reports/`, so they do not trigger the function again.
7. Upload `sample.log` to the bucket under the `logs/` prefix (the S3 key must be `logs/sample.log`).
8. Open the Lambda function's Monitor tab and view CloudWatch logs. Check the S3 bucket for `reports/sample.log.summary.json`.

## Test checklist

- [ ] Lambda invocation appears in CloudWatch Logs
- [ ] Report JSON is created under `reports/`
- [ ] Report has the correct line total and level counts
- [ ] Bucket remains private

## Important safety and cleanup

- Do not upload confidential, personal or production logs.
- Keep S3 Block Public Access enabled.
- Do not grant `s3:*` or public access for this demo; use the narrow permissions above.
- Check AWS Billing and Free Tier before deploying; eligibility and charges depend on your account and usage.
- When finished, delete the test objects, Lambda function, and demo bucket if you no longer need them. Empty the bucket before deleting it. Remove any IAM policy/role created solely for this project if it is no longer needed.

## Resume bullet (use only after completing and testing)

Built an event-driven log analysis workflow using Amazon S3, AWS Lambda (Python), IAM and CloudWatch; automatically processed uploaded logs, counted severity levels, and generated JSON summaries with least-privilege storage permissions.

## LinkedIn post template (edit after successful testing)

Built a small AWS serverless project: **Serverless Log Analyzer**.

When a log file is uploaded to Amazon S3, an S3 event triggers a Python AWS Lambda function. The function counts INFO, WARNING, ERROR and DEBUG entries and writes a JSON summary back to S3. I used IAM permissions to restrict access to the input and output prefixes and CloudWatch Logs to verify execution.

**What I practiced:** S3 event notifications, serverless compute, event-driven architecture, IAM least privilege, and CloudWatch troubleshooting.

Next improvement: add a dashboard or alerting for repeated errors.

#AWS #AWSLambda #AmazonS3 #CloudComputing #DevOps #Python
