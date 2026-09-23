def get_op_packing_only_uses_module_attributes(
    op: Callable,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    module: torch.nn.Module,
) -> bool:
    """
    Returns True if all arguments of this op which are weights are module
    attributes on the root module, and False otherwise.

    For example, for `F.linear(input, weight, bias)`, this would return
    True if `weight` is stored directly on the parent module (the common case),
    and False if `weight` was an output of a different op.
    """
    # check for ops which need packed weights but the weights are
    # coming from another function
    info = get_weight_argument_info(op)
    if info is not None:
        idx, name = info
        param_name = args[idx] if idx < len(args) else kwargs[name]
        arg_name_in_root = get_param_name(module, param_name)
        if arg_name_in_root is None:
            return False
    return True
