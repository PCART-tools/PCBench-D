def reduce_sum(model, blob_in, blob_out, **kwargs):
    """ReduceSum"""
    return model.net.ReduceSum(blob_in, blob_out, **kwargs)
