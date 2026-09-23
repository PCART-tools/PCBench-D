def mat_mul(model, blob_in, blob_out, **kwargs):
    """Matrix multiplication"""
    return model.net.MatMul(blob_in, blob_out, **kwargs)
