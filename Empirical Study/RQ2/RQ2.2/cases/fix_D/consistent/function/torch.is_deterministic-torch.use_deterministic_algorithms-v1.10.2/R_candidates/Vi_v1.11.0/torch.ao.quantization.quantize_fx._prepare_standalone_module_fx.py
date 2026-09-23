def _prepare_standalone_module_fx(
    model: torch.nn.Module,
    qconfig_dict: Any,
    is_qat: bool,
    prepare_custom_config_dict: Optional[Dict[str, Any]] = None,
    backend_config_dict: Optional[Dict[str, Any]] = None,
) -> GraphModule:
    r""" [Internal use only] Prepare a standalone module, so that it can be used when quantizing the
    parent module.
    standalone_module means it a submodule that is not inlined in parent module,
    and will be quantized separately as one unit.

    How the standalone module is observed is specified by `input_quantized_idxs` and
    `output_quantized_idxs` in the prepare_custom_config for the standalone module

    Returns:

        * model(GraphModule): prepared standalone module. It has these attributes:

            * `_standalone_module_input_quantized_idxs(List[Int])`: a list of
              indexes for the graph input that is expected to be quantized,
              same as input_quantized_idxs configuration provided
              for the standalone module
            * `_standalone_module_output_quantized_idxs(List[Int])`: a list of
              indexs for the graph output that is quantized
              same as input_quantized_idxs configuration provided
              for the standalone module

    """
    return _prepare_fx(
        model,
        qconfig_dict,
        is_qat,
        prepare_custom_config_dict,
        backend_config_dict=backend_config_dict,
        is_standalone_module=True,
    )
