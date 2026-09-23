def sparse_lengths_sum_4bit_rowwise_sparse(model, blob_in, blob_out, **kwargs):
    return model.net.SparseLengthsSum4BitRowwiseSparse(blob_in, blob_out, **kwargs)
