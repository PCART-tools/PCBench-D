def get_S3_object_from_bucket(bucket_name: str, object: str) -> Any:
    return S3_RESOURCE.Object(bucket_name, object)
