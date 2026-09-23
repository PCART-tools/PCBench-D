def weight_dtype(qconfig):
    assert qconfig is not None
    weight = qconfig.weight()
    return weight.dtype
