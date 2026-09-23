def FetchInt8Blob(name):
    """Fetches an Int8 blob from the workspace. It shared backend implementation
    with FetchBlob but it is recommended when fetching Int8 Blobs

    Inputs:
      name: the name of the Int8 blob - a string or a BlobReference
    Returns:
      data: int8 numpy array, data
      scale: float, fake quantization scale
      zero_point: int, fake quantization offset
    """
    result = C.fetch_blob(StringifyBlobName(name))
    assert isinstance(result, tuple), \
        'You are not fetching an Int8Blob {}. Please use FetchBlob'.format(
            StringifyBlobName(name))
    return Int8Tensor(*result)
