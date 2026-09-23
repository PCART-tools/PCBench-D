def get_cpp_op_schema(kernel: torch._ops.OpOverload) -> str:
    args = kernel._schema.arguments
    returns = kernel._schema.returns

    num_returns = len(returns)
    assert num_returns > 0, "must have at least one return value"

    if num_returns == 1:
        cpp_return_value = convert_return_type(returns[0])
    elif num_returns > 1:
        tuple_returns = ", ".join([convert_return_type(r) for r in returns])
        cpp_return_value = f"std::tuple<{tuple_returns}>"

    cpp_arg_type = [f"{convert_arg_type(arg)} {arg.name}" for arg in args]
    return f"{cpp_return_value}({', '.join(cpp_arg_type)})"  # type: ignore[possibly-undefined]
