def _is_supported_cloud(file: str) -> bool:
    return file.startswith(("s3", "gs", "az", "adl", "abfs"))
