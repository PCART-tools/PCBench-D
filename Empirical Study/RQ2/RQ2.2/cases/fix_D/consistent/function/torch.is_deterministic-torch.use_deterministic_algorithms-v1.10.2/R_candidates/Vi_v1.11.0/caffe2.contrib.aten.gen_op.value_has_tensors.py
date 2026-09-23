def value_has_tensors(v):
    # Sparse shouldn't appear in public API, seems to be temporary bug
    return "Tensor" in v['dynamic_type'] and "Sparse" not in v['dynamic_type']
