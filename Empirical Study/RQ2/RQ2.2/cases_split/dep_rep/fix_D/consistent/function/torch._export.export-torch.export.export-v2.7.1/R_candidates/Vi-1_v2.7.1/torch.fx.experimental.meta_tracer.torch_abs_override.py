def torch_abs_override(input, *, out=None):
    assert out is None, "Dont support in-place abs for MetaTensor analysis"
    return input
