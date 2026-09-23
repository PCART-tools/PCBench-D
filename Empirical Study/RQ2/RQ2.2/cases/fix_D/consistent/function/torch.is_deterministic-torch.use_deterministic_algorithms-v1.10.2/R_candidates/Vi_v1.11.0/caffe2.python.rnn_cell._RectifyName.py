def _RectifyName(blob_reference_or_name):
    if blob_reference_or_name is None:
        return None
    if isinstance(blob_reference_or_name, str):
        return core.ScopedBlobReference(blob_reference_or_name)
    if not isinstance(blob_reference_or_name, core.BlobReference):
        raise Exception("Unknown blob reference type")
    return blob_reference_or_name
