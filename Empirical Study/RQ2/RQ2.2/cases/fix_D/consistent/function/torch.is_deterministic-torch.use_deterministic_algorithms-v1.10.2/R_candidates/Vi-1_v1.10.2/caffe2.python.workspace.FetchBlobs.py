def FetchBlobs(names):
    """Fetches a list of blobs from the workspace.

    Inputs:
        names: list of names of blobs - strings or BlobReferences
    Returns:
        list of fetched blobs
    """
    return [FetchBlob(name) for name in names]
