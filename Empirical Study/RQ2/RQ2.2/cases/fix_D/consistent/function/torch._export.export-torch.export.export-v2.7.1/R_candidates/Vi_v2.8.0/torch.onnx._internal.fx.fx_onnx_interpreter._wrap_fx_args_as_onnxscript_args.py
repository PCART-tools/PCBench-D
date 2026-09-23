def _wrap_fx_args_as_onnxscript_args(
    complete_args: list[fx_type_utils.Argument],
    complete_kwargs: dict[str, fx_type_utils.Argument],
    fx_name_to_onnxscript_value: dict[
        str,
        onnxscript_graph_building.TorchScriptTensor
        | tuple[onnxscript_graph_building.TorchScriptTensor, ...],
    ],
    tracer: onnxscript_graph_building.TorchScriptTracingEvaluator,
) -> tuple[
    Sequence[
        onnxscript_graph_building.TorchScriptTensor
        | str
        | int
        | float
        | bool
        | list
        | complex
        | None
    ],
    dict[str, fx_type_utils.Argument],
]:
    """Map all FX arguments of a node to arguments in TorchScript graph."""

    onnxscript_args = tuple(
        _retrieve_or_adapt_input_to_graph_set(arg, fx_name_to_onnxscript_value, tracer)
        for arg in complete_args
    )
    onnxscript_kwargs = filter_incompatible_and_dtype_convert_kwargs(complete_kwargs)

    return onnxscript_args, onnxscript_kwargs
