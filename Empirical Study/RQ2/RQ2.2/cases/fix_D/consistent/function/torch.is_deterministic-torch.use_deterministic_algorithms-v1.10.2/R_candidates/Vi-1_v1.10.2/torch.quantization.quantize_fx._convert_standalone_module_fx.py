def _convert_standalone_module_fx(
        graph_module: GraphModule, is_reference: bool = False,
        convert_custom_config_dict: Dict[str, Any] = None) -> QuantizedGraphModule:
    r""" [Internal use only] Convert a model produced by :func:`~torch.quantization.prepare_standalone_module_fx`
    and convert it to a quantized model

    Returns a quantized standalone module, whether input/output is quantized is
    specified by prepare_custom_config_dict, with
    input_quantized_idxs, output_quantized_idxs, please
    see docs for prepare_fx for details
    """
    return _convert_fx(graph_module, is_reference, convert_custom_config_dict, is_standalone_module=True)
