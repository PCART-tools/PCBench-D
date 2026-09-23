def sum(model, blob_in, blob_out, **kwargs):
    """Sum"""
    return model.net.Sum(blob_in, blob_out, **kwargs)
