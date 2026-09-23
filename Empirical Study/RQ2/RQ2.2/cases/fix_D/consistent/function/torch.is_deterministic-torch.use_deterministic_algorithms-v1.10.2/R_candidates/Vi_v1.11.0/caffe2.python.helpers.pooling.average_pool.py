def average_pool(model, blob_in, blob_out, use_cudnn=False, order="NCHW",
                 **kwargs):
    """Average pooling"""
    if use_cudnn:
        kwargs['engine'] = 'CUDNN'
    return model.net.AveragePool(
        blob_in,
        blob_out,
        order=order,
        **kwargs
    )
