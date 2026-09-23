def batch_mat_mul(model, blob_in, blob_out,
                  enable_tensor_core=False, **kwargs):
    if enable_tensor_core:
        kwargs['engine'] = 'TENSORCORE'

    return model.net.BatchMatMul(blob_in, blob_out, **kwargs)
