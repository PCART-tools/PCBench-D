def FetchInt8BlobRealVal(name):
    """Fetches an Int8 blob from the workspace and return its real value representation.

    Inputs:
      name: the name of the Int8 blob - a string or a BlobReference
    Returns:
      real value representation of int8 numpy array
    """
    result = C.fetch_blob(StringifyBlobName(name))
    assert isinstance(result, tuple), \
        'You are not fetching an Int8Blob {}. Please use FetchBlob'.format(
            StringifyBlobName(name))
    int8_blob = Int8Tensor(*result)
    return (int8_blob.data.astype(np.int32) - int(int8_blob.zero_point)).astype(
        np.float32) * int8_blob.scale
