def get_S3_bucket_readonly(bucket_name: str) -> Any:
    return S3_RESOURCE_READ_ONLY.Bucket(bucket_name)
