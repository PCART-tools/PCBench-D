def get_quantize_node_info(activation_post_process: Callable) -> Tuple[str, Union[Callable, str], Dict[str, Any]]:
    ''' Given an activation_post_process module,
    return node_type(e.g. call_function), quantize op(e.g. quantize_per_tensor) and a dictionary
    of extracted qparams from the module
    '''
    dtype = activation_post_process.dtype  # type: ignore[attr-defined]
    quantize_op : Optional[Union[Callable, str]] = None
    if dtype in [torch.quint8, torch.qint8]:
        node_type = "call_function"
        scale, zero_point = activation_post_process.calculate_qparams()  # type: ignore[attr-defined]
        if is_per_channel(activation_post_process.qscheme):  # type: ignore[attr-defined]
            ch_axis = int(activation_post_process.ch_axis)  # type: ignore[attr-defined]
            qparams = {"_scale_": scale, "_zero_point_": zero_point, "_axis_": ch_axis, "_dtype_": dtype}
            quantize_op = torch.quantize_per_channel
        else:
            scale = float(scale)
            zero_point = int(zero_point)
            qparams = {"_scale_": scale, "_zero_point_": zero_point, "_dtype_": dtype}
            quantize_op = torch.quantize_per_tensor
    elif dtype == torch.float16:
        node_type = "call_method"
        quantize_op = "to"
        qparams = {"_dtype_": dtype}
    else:
        raise Exception("Unsupported dtype in get_quantize_node_info:" + str(dtype))
    assert quantize_op is not None
    return node_type, quantize_op, qparams
