def attach_output_convert_info_to_model(
    module: torch.nn.Module,
) -> None:
    """
    Calculates the info needed to perform the module outputs hook
    and attaches it to the parent module. This is done to avoid recalculating
    these values at inference.
    """
    if hasattr(module, '_auto_quant_state'):
        qstate: AutoQuantizationState = module._auto_quant_state  # type: ignore[assignment]
        qstate.set_needs_dtype_transform_on_outputs()

    for _, child in module.named_children():
        attach_output_convert_info_to_model(child)
