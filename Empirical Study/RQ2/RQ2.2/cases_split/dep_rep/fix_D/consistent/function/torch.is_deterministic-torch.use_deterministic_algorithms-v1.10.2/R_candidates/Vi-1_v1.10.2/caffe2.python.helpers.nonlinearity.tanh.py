def tanh(model, blob_in, blob_out, use_cudnn=False, order="NCHW", **kwargs):
    """Tanh."""
    if use_cudnn:
        kwargs['engine'] = 'CUDNN'
    return model.net.Tanh(blob_in, blob_out, order=order, **kwargs)
