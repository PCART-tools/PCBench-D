def all_symbolics_schemas() -> dict[str, _TorchSchema]:
    """Returns schemas for all onnx supported ops."""
    symbolics_schemas = {}

    for name in registration.registry.all_functions():
        func_group = registration.registry.get_function_group(name)
        assert func_group is not None
        symbolics_schema = _TorchSchema(name)
        func = func_group.get(_constants.ONNX_MAX_OPSET)
        if func is not None:
            symbolics_schema.arguments = _symbolic_argument_count(func)
            symbolics_schema.opsets = list(
                range(func_group.get_min_supported(), _constants.ONNX_MAX_OPSET + 1)
            )
        else:
            # Only support opset < 9
            func = func_group.get(7)
            symbolics_schema.arguments = _symbolic_argument_count(func)
            symbolics_schema.opsets = list(range(7, _constants.ONNX_BASE_OPSET))

        symbolics_schemas[name] = symbolics_schema

    return symbolics_schemas
