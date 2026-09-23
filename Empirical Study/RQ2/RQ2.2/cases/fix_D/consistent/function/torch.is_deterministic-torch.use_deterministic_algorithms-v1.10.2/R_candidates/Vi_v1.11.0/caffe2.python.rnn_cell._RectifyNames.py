def _RectifyNames(blob_references_or_names):
    if blob_references_or_names is None:
        return None
    return [_RectifyName(i) for i in blob_references_or_names]
