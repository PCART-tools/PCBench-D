def op_is_int8_dynamically_quantized(qconfig) -> bool:
    """ Given a qconfig, returns True if this op is using int8 dynamic
    quantization
    """
    activation_dtype, weight_dtype, activation_compute_dtype = \
        get_qconfig_dtypes(qconfig)
    return (
        activation_dtype is torch.float and
        # for now, the lines below assume fbgemm or qnnpack
        weight_dtype is torch.qint8 and
        activation_compute_dtype is torch.quint8
    )
