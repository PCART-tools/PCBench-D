def dropout(model, blob_in, blob_out, use_cudnn=False, **kwargs):
    """dropout"""
    if use_cudnn:
        kwargs['engine'] = 'CUDNN'
    else:
        kwargs['engine'] = 'DEFAULT'
    assert 'is_test' in kwargs, "Argument 'is_test' is required"
    return model.net.Dropout(
        blob_in, [blob_out, "_" + blob_out + "_mask"], **kwargs)[0]
