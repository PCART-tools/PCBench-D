def get_static_sparse_quantized_mapping():
    _static_sparse_quantized_mapping = dict({
        torch.nn.Linear: torch.ao.nn.sparse.quantized.Linear,
    })
    return _static_sparse_quantized_mapping
