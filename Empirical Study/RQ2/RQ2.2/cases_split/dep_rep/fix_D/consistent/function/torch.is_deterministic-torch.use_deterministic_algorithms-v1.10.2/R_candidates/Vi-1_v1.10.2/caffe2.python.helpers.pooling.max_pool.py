def max_pool(model, blob_in, blob_out, use_cudnn=False, order="NCHW", **kwargs):
    """Max pooling"""
    if use_cudnn:
        kwargs['engine'] = 'CUDNN'
    return model.net.MaxPool(blob_in, blob_out, order=order, **kwargs)
