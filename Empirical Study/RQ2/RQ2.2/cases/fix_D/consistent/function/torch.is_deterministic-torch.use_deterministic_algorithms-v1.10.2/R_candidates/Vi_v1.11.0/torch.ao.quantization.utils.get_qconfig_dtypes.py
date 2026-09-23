def get_qconfig_dtypes(qconfig):
    r""" returns the qconfig tuple for qconfig:
    (activation_dtype, weight_dtype, activation_compute_dtype)
    """
    assert qconfig is not None
    activation = qconfig.activation()
    weight = qconfig.weight()
    compute_dtype = activation.compute_dtype if hasattr(activation, 'compute_dtype') else None
    return (activation.dtype, weight.dtype, compute_dtype)
