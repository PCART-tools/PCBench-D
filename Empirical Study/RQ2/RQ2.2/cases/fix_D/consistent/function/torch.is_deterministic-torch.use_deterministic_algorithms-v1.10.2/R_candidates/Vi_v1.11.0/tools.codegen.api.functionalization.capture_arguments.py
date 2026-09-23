def capture_arguments(func: FunctionSchema, *, is_reverse: bool) -> List[Binding]:
    # capture arguments include all arguments except `self`.
    # Importantly, they don't include any C++ reference types (or else we'll get a dangling reference in the capture),
    # So any reference types (IntArrayRef) need to be converted to value types (vector<int64_t>)
    args = func.arguments.flat_all
    assert args[0].type == BaseType(BaseTy.Tensor)
    non_self_args = args[1:]
    non_self_value_bindings = [dispatcher.argument(a, remove_non_owning_ref_types=True) for a in non_self_args]
    return non_self_value_bindings
