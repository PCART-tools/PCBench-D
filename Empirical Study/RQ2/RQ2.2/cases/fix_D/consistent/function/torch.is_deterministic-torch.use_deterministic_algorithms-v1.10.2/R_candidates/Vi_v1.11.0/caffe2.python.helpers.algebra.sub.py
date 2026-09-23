def sub(model, blob_in, blob_out, **kwargs):
    """Subtract"""
    return model.net.Sub(blob_in, blob_out, **kwargs)
