# AWS Serverless Log Analyzer

An event-driven serverless project that automatically analyzes log files uploaded to Amazon S3. An S3 event triggers a Python AWS Lambda function, which counts log severity levels and saves a JSON summary back to S3.

## Architecture

```text
Upload sample.log
       |
       v
Amazon S3 (logs/)
       |
       | S3 ObjectCreated event
       v
AWS Lambda (Python + boto3)
       |
       | Analyze log severity levels
       v
Amazon S3 (reports/)
       |
       v
sample.log.summary.json

CloudWatch Logs -> Execution monitoring and troubleshooting
```

## AWS Services and Technologies

- **Amazon S3:** Stores input log files and generated JSON reports.
- **AWS Lambda:** Runs the log analyzer automatically in response to S3 events.
- **AWS IAM:** Controls Lambda's access to input and output objects.
- **Amazon CloudWatch Logs:** Records execution messages and helps troubleshoot errors.
- **Python and boto3:** Process log text and interact with AWS services.
- **JSON:** Stores the analysis results in a structured format.

## Project Structure

```text
aws-serverless-log-analyzer/
├── lambda_function.py
├── sample.log
├── sample_expected_report.json
└── README.md
```

## Verified Test Results

Uploaded `logs/sample.log` to the S3 bucket and verified that Lambda generated:

`reports/sample.log.summary.json`

The generated report contained these results:

| Metric | Verified count |
|---|---:|
| Total log lines | 7 |
| ERROR | 2 |
| WARNING | 1 |
| INFO | 3 |
| DEBUG | 1 |

## How It Works

1. A log file is uploaded under the S3 `logs/` prefix.
2. An S3 object-created event triggers the Lambda function.
3. Lambda reads the log file and counts INFO, WARNING, ERROR, and DEBUG entries.
4. Lambda writes a JSON summary under the S3 `reports/` prefix.
5. CloudWatch Logs records execution messages for troubleshooting.

The S3 trigger uses the `logs/` prefix to avoid repeatedly processing reports written under `reports/`.

## Deployment Guide

1. Create a private S3 bucket in your chosen AWS Region. Keep Block Public Access enabled.
2. Create a Lambda execution role with CloudWatch logging permissions.
3. Add a narrowly scoped IAM policy allowing `s3:GetObject` on `logs/*` and `s3:PutObject` on `reports/*` for your bucket.
4. Create the `serverless-log-analyzer` Lambda function using a Python 3.x runtime.
5. Deploy the code from `lambda_function.py`.
6. Configure an S3 trigger for all object-created events with the prefix `logs/`.
7. Upload `sample.log` as `logs/sample.log`.
8. Verify the generated report at `reports/sample.log.summary.json` and inspect the Lambda execution logs in CloudWatch.

Replace `YOUR_BUCKET_NAME` with your own bucket name when configuring IAM resources. Use the same AWS Region for the S3 bucket and Lambda function.

## Security and Cost Considerations

- Keep the S3 bucket private.
- Grant only the permissions required to read input logs and write reports.
- Never commit AWS credentials, access keys, passwords, or confidential logs.
- Review AWS Billing and Free Tier usage because charges depend on your account and usage.
- Delete test resources you no longer need. Empty the S3 bucket before deleting it, and remove dedicated IAM policies or roles only when they are no longer needed.

## Skills Demonstrated

AWS serverless computing, event-driven architecture, Amazon S3 event notifications, AWS Lambda, IAM permissions, CloudWatch troubleshooting, Python, boto3, and JSON processing.

## Future Improvements

- Add automated unit tests.
- Add error notifications using Amazon SNS.
- Build a dashboard showing log severity trends.
- Add structured logging and more robust handling of malformed log files.

## Resume Bullet

Built and tested an event-driven AWS serverless log analyzer using Amazon S3, AWS Lambda, Python, IAM, and CloudWatch to process uploaded log files and automatically generate JSON severity summaries.

## LinkedIn Post

I’m excited to share a hands-on cloud project I built: **AWS Serverless Log Analyzer**.

The project uses Amazon S3 and AWS Lambda to automate log analysis. When a log file is uploaded to S3, an event triggers a Python function that counts INFO, WARNING, ERROR, and DEBUG entries and generates a JSON report.

**What I learned and practiced:**
- Event-driven architecture using Amazon S3 notifications
- Serverless computing with AWS Lambda
- IAM permissions and least-privilege access
- CloudWatch Logs for execution monitoring and troubleshooting
- Python, boto3, and JSON processing

I tested the workflow by uploading a sample log file and verified that the generated report contained the expected severity counts.

Next, I plan to explore automated testing, alerting, and dashboard integration.

GitHub: https://github.com/kshitijpawar3777-del/aws-serverless-log-analyzer

#AWS #AWSLambda #AmazonS3 #CloudComputing #DevOps #Python #CloudProjects
