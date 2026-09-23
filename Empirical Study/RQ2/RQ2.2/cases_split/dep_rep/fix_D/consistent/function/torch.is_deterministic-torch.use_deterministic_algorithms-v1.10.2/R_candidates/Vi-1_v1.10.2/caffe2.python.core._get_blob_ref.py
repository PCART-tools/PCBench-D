def _get_blob_ref(blob_name_or_ref):
    return (
        blob_name_or_ref if isinstance(input, BlobReference)
        else BlobReference(blob_name_or_ref)
    )
