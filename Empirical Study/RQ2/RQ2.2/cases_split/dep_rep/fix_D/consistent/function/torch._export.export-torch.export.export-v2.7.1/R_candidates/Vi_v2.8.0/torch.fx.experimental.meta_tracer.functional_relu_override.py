def functional_relu_override(x, inplace=False):
    assert not inplace, "dont support inplace functional.relu for metatensor analysis"
    return x
