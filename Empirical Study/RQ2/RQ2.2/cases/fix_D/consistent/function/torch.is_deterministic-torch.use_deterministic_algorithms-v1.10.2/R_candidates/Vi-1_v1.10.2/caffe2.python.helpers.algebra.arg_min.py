def arg_min(model, blob_in, blob_out, **kwargs):
    """ArgMin"""
    return model.net.ArgMin(blob_in, blob_out, **kwargs)
