def get_matching_overload(
    node: torch.fx.Node,
    overloads: Sequence[_registration.OnnxDecompMeta],
) -> tuple[Callable | None, str]:
    """Get the overload that matches the node's arguments.

    Args:
        node: The node to match.
        overloads: The OnnxDecompMeta with overloads and their signatures to match against.

    Returns:
        A tuple containing the matched overload and a string describing the reason for failure or success.
    """
    if not hasattr(node.target, "_schema"):
        # FIXME(justinchuby): When the target is a builtin, we should instead
        # Match only the inputs positionally. Figure out how to do that as right
        # now we assume all inputs are named.
        return overloads[
            0
        ].onnx_function, "The node target does not have a schema. Return the first one."
    named_args = _get_named_fx_node_args(node)
    # FIXME: Handle when we don't know the names of the arguments
    schema_args: dict[str, torch.Argument] = {
        arg.name: arg
        for arg in node.target._schema.arguments  # type: ignore[union-attr]
    }
    failure_messages: list[str] = []
    for overload in overloads:
        assigned_types: dict[str, ir.TypeProtocol] = {}
        fail_reason = ""
        if overload.signature is None:
            # When an overload does not have a signature, we assume it is a custom op and should be matched
            return (
                overload.onnx_function,
                "The overload does not have a signature. Assuming it is a custom op and matching it.",
            )
        for param in overload.signature:
            if param.name not in schema_args and param.required:
                # We don't need to handle variadic inputs as there is none.
                # A required parameter is not supplied.
                fail_reason = "Required parameter not supplied"
                break

            # Get the argument
            if param.name in named_args:
                # Provided in Node args
                arg = named_args[param.name]
            elif (
                param.name in schema_args
                and schema_args[param.name].has_default_value()
            ):
                # Provided in schema args
                arg = schema_args[param.name].default_value
            elif param.has_default():
                # Provided in the ONNX op definition
                arg = param.default  # type: ignore[assignment]
            else:
                fail_reason = "Parameter not provided"
                break

            if isinstance(param, _schemas.Parameter):
                if isinstance(arg, torch.Tensor):
                    arg = _get_type_from_tensor(arg)  # type: ignore[assignment]
                if isinstance(arg, (list, tuple)) and any(
                    isinstance(t, torch.fx.Node) for t in arg
                ):
                    first_tensor = _get_first_tensor_in_node_list(arg)  # type: ignore[arg-type]
                    assert first_tensor is not None
                    # FIXME: Handle symfloat here
                    arg = ir.SequenceType(_get_type_from_tensor(first_tensor))  # type: ignore[assignment]
                elif isinstance(arg, torch.fx.Node):
                    meta_val = arg.meta["val"]
                    arg = _get_type_from_tensor(meta_val)  # type: ignore[assignment]
                # TODO: Handle None attributes
                # FIXME: Handle symfloat etc.
                # Handle tensors and Python values
                if not _param_type_compatible_with_arg(param, arg, assigned_types):  # type: ignore[arg-type]
                    fail_reason = (
                        f"Parameter type not compatible with argument: param=`{param}`, "
                        f"assigned_types=`{assigned_types}`, arg=`{arg}`"
                    )
                    break
            elif isinstance(param, _schemas.AttributeParameter):
                if not _attribute_type_compatible_with_arg(param, arg):  # type: ignore[arg-type]
                    fail_reason = f"Attribute type not compatible with argument: param=`{param}`, arg=`{arg}`"
                    break
            else:
                raise TypeError(f"Unknown parameter type: {type(param)}")
        if not fail_reason:
            return overload.onnx_function, "Successfully matched overload"
        else:
            failure_messages.append(
                f"- Failed to match overload `{overload}`: {fail_reason}"
            )
    return (
        None,
        f"All overloads did not match the node `{node.format_node()}`.\n"
        + "\n".join(failure_messages),
    )
