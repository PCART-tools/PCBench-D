def _unwrap_tensoralias(x):
    assert isinstance(x, TensorAlias)
    return x.alias
