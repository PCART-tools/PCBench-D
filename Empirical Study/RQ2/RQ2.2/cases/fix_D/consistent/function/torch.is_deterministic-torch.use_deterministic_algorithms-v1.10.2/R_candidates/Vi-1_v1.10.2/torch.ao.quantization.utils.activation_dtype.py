def activation_dtype(qconfig):
    assert qconfig is not None
    activation = qconfig.activation()
    return activation.dtype
