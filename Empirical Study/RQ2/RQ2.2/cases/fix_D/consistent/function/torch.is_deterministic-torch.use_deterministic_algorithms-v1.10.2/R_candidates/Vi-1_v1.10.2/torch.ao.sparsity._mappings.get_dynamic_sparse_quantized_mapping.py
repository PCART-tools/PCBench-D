def get_dynamic_sparse_quantized_mapping():
    _dynamic_sparse_quantized_mapping = dict({
        torch.nn.Linear: torch.ao.nn.sparse.quantized.dynamic.Linear,
    })
    return _dynamic_sparse_quantized_mapping
