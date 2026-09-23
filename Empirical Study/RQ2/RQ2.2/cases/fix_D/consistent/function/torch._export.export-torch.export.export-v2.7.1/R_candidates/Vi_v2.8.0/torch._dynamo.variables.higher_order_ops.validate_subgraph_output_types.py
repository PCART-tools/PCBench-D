def validate_subgraph_output_types(output: VariableTracker):
    """Verify that that the output of the subgraph is a tensor,
    int, bool, SymBool, or SymInt.
    """
    from . import TensorVariable

    if non_tensor_output := find_mismatched_vars(
        output, TensorVariable, allow_none=True
    ):
        for out in non_tensor_output:
            if (
                isinstance(out, SymNodeVariable) and out.python_type() in (int, bool)
            ) or (
                isinstance(out, ConstantVariable) and out.python_type() in (int, bool)
            ):
                continue
            unimplemented(
                f"HigherOrderOperator body's output must consist of tensors or ints only but got {out.python_type()}"
            )
