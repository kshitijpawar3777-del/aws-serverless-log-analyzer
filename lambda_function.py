import boto3
import json
import os
from urllib.parse import unquote_plus
from datetime import datetime, timezone

s3 = boto3.client("s3")

def lambda_handler(event, context):
    """
    Triggered by an S3 ObjectCreated event for files under logs/.
    Reads a text log, counts common log levels, and writes a JSON report
    under reports/ in the same bucket. Configure the S3 trigger to only
    watch the logs/ prefix so report uploads do not trigger this function.
    """
    processed = []

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

        # Safety guard: only process files uploaded to the input prefix.
        if not key.startswith("logs/") or key.endswith("/"):
            continue

        response = s3.get_object(Bucket=bucket, Key=key)
        raw_text = response["Body"].read().decode("utf-8", errors="replace")
        lines = [line for line in raw_text.splitlines() if line.strip()]

        counts = {"ERROR": 0, "WARNING": 0, "INFO": 0, "DEBUG": 0}
        error_examples = []

        for line in lines:
            upper = line.upper()
            for level in counts:
                if level in upper:
                    counts[level] += 1
                    if level == "ERROR" and len(error_examples) < 5:
                        error_examples.append(line[:300])
                    break

        report = {
            "source_bucket": bucket,
            "source_key": key,
            "processed_at_utc": datetime.now(timezone.utc).isoformat(),
            "total_non_empty_lines": len(lines),
            "log_level_counts": counts,
            "error_examples": error_examples
        }

        filename = key.rsplit("/", 1)[-1]
        report_key = f"reports/{filename}.summary.json"
        s3.put_object(
            Bucket=bucket,
            Key=report_key,
            Body=json.dumps(report, indent=2).encode("utf-8"),
            ContentType="application/json"
        )

        print(json.dumps({
            "message": "Log analysis completed",
            "source_key": key,
            "report_key": report_key,
            "total_non_empty_lines": len(lines),
            "log_level_counts": counts
        }))
        processed.append({"source": key, "report": report_key})

    return {"statusCode": 200, "processed_files": processed}
