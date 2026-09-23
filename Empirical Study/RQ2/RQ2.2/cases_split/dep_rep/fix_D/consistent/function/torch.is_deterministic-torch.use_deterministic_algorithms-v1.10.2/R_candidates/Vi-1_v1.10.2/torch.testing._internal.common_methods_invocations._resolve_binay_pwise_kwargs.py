def _resolve_binay_pwise_kwargs(
        op_info, *, op_kwargs=None, lhs_make_tensor_kwargs=None, rhs_make_tensor_kwargs=None
):
    """Resolves default values for :func:`sample_inputs_binary_pwise`.

    By default :attr:`op_kwargs`, :attr:`lhs_make_tensor_kwargs`, and :attr:`rhs_make_tensor_kwargs` are just empty
    dictionaries. In case :attr:`op_info` is a :class:`BinaryUfuncInfo`, :attr:`BinaryUfuncInfo.lhs_make_tensor_kwargs`
    and :attr:`BinaryUfuncInfo.rhs_make_tensor_kwargs` will be used as defaults.
    """
    if op_kwargs is None:
        op_kwargs = {}
    if lhs_make_tensor_kwargs is None:
        lhs_make_tensor_kwargs = op_info.lhs_make_tensor_kwargs if isinstance(op_info, BinaryUfuncInfo) else {}
    if rhs_make_tensor_kwargs is None:
        rhs_make_tensor_kwargs = op_info.rhs_make_tensor_kwargs if isinstance(op_info, BinaryUfuncInfo) else {}

    return op_kwargs, lhs_make_tensor_kwargs, rhs_make_tensor_kwargs
