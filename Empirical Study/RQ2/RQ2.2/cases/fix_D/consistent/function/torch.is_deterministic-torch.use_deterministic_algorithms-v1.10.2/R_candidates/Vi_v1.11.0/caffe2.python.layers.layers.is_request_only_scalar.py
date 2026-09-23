def is_request_only_scalar(scalar):
    if len(scalar.field_metadata()) == 0:
        return False
    for metadata in scalar.field_metadata():
        if not (
            metadata
            and metadata.feature_specs
            and getattr(metadata.feature_specs, "feature_is_request_only", False)
        ):
            return False
    return True
