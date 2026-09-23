def _normalize_field(field_or_type_or_blob, keep_blobs=True):
    """Clones/normalizes a field before adding it to a container."""
    if isinstance(field_or_type_or_blob, Field):
        return field_or_type_or_blob.clone(keep_blobs=keep_blobs)
    elif type(field_or_type_or_blob) in (type, np.dtype):
        return Scalar(dtype=field_or_type_or_blob)
    else:
        return Scalar(blob=field_or_type_or_blob)
