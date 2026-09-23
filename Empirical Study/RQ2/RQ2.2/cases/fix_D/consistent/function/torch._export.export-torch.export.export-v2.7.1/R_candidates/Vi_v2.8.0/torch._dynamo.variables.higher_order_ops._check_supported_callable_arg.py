def _check_supported_callable_arg(
    tx: "InstructionTranslator", func_var: VariableTracker, arg_name
):
    is_callable = (
        BuiltinVariable(callable).call_function(tx, [func_var], {}).as_python_constant()
    )
    if not is_callable:
        unimplemented(
            f"{arg_name} should be a Callable but is of type {str(func_var)}."
        )
