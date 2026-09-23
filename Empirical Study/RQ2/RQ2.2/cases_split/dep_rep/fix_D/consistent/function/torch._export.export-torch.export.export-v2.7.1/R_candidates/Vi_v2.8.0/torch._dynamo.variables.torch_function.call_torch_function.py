def call_torch_function(tx, torch_function_var, fn, types, args, kwargs):
    # This emulates calling __torch_function__, which has a signature
    #   def __torch_function__(cls, func, types, args=(), kwargs=None):
    #
    # Also notice the `cls` is not explicitly passed in the reference
    # implementations:
    # 1. https://github.com/pytorch/pytorch/blob/8d81806211bc3c0ee6c2ef235017bacf1d775a85/torch/csrc/utils/python_arg_parser.cpp#L368-L374  # noqa: B950
    # 2. https://github.com/pytorch/pytorch/blob/8d81806211bc3c0ee6c2ef235017bacf1d775a85/torch/overrides.py#L1741-L1743
    tf_args = [
        fn,
        types,
        VariableTracker.build(tx, tuple(args)),
        VariableTracker.build(tx, kwargs),
    ]
    return torch_function_var.call_function(tx, tf_args, {})
