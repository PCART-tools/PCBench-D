def get_quant_type(qconfig):
    assert qconfig is not None
    activation = qconfig.activation()
    weight = qconfig.weight()
    static_dtypes = [torch.quint8, torch.qint8]
    if weight.dtype in static_dtypes:
        if activation.dtype in static_dtypes:
            return QuantType.STATIC
        elif hasattr(activation, 'compute_dtype') and activation.compute_dtype in static_dtypes:
            return QuantType.DYNAMIC
        else:
            return QuantType.WEIGHT_ONLY

    if weight.dtype == torch.float16:
        if activation.dtype == torch.float:
            return QuantType.DYNAMIC
        elif activation.dtype == torch.float16:
            return QuantType.STATIC

    raise Exception("Unrecognized dtype combination in get_quant_type: activation({}),"
                    "weight({})".format(activation.dtype, weight.dtype))
