def _Blob_to_torch(blob):
    if not blob.is_tensor():
        raise RuntimeError("Blob has to be a tensor")
    return blob.as_tensor().to_torch()
