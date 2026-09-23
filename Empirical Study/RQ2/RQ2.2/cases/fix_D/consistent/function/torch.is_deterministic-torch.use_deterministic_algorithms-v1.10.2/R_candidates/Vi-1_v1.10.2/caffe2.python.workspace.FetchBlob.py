def FetchBlob(name):
    """Fetches a blob from the workspace.

    Inputs:
      name: the name of the blob - a string or a BlobReference
    Returns:
      Fetched blob (numpy array or string) if successful
    """
    result = C.fetch_blob(StringifyBlobName(name))
    if isinstance(result, tuple):
        raise TypeError(
            "Use FetchInt8Blob to fetch Int8 Blob {}".format(
                StringifyBlobName(name)
            )
        )
    return result
