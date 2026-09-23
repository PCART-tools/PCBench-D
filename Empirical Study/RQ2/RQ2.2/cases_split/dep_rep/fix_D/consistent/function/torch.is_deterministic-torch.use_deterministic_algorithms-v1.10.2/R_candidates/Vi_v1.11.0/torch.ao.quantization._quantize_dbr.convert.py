def convert(model: torch.nn.Module) -> torch.nn.Module:
    r"""Converts a prepared DBR quantization model to a quantized form.

    TODO(future PR): better docblock
    """
    static_mappings = get_default_static_quant_module_mappings()
    dynamic_mappings = get_default_dynamic_quant_module_mappings()
    # swap the modules
    _swap_child_modules(model, static_mappings, dynamic_mappings)
    # add dynamic handling for quants/dequants, functions and methods
    model = add_auto_convert(model)
    return model
