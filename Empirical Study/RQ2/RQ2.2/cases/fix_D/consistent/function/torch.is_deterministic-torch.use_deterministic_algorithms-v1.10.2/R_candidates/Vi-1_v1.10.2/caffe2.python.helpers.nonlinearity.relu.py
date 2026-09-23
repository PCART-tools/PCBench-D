def relu(model, blob_in, blob_out, use_cudnn=False, order="NCHW", **kwargs):
    """Relu."""
    if use_cudnn:
        kwargs['engine'] = 'CUDNN'
    return model.net.Relu(blob_in, blob_out, order=order, **kwargs)
