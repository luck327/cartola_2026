"""Shared helpers for S3 persistence."""

import json
from datetime import UTC, datetime

import boto3

s3 = boto3.client("s3")


def exists_prefix(bucket_name: str, prefix: str) -> bool:
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, MaxKeys=1)
    return "Contents" in response


def save_json(bucket_name: str, key: str, payload: dict) -> None:
    s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(payload))
    print(f"📦 Salvo em s3://{bucket_name}/{key}")


def timestamp_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H-%M-%S")
