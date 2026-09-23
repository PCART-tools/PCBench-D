def _is_arg_with_complex_dtype(arg: fx_type_utils.Argument) -> bool:
    """Check if the node has complex dtype recursively."""
    if (
        isinstance(arg, torch.fx.Node)
        and "val" in arg.meta
        and isinstance(arg.meta["val"], torch.Tensor)
        and torch.is_complex(arg.meta["val"])
    ):
        return True
    elif isinstance(arg, list):
        for item in arg:
            return _is_arg_with_complex_dtype(item)
    return False
