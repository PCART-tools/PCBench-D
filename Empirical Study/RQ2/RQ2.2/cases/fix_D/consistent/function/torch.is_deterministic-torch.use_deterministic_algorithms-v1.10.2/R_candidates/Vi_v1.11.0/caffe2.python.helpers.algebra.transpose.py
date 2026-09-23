def transpose(model, blob_in, blob_out, use_cudnn=False, **kwargs):
    """Transpose."""
    if use_cudnn:
        kwargs['engine'] = 'CUDNN'
    return model.net.Transpose(blob_in, blob_out, **kwargs)
