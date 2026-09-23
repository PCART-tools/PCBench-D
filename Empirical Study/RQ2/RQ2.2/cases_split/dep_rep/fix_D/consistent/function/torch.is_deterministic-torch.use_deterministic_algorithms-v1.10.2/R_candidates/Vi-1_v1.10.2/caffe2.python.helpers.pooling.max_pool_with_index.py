def max_pool_with_index(model, blob_in, blob_out, order="NCHW", **kwargs):
    """Max pooling with an explicit index of max position"""
    return model.net.MaxPoolWithIndex(
        blob_in,
        [blob_out, blob_out + "_index"],
        order=order,
        **kwargs
    )[0]
