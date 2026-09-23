def attach_scale_zp_values_to_model(
    module: torch.nn.Module,
) -> None:
    """
    Calculates the scale and zero_point from each observer and attaches
    these values to the parent module. This is done to avoid recalculating
    these values at inference.
    """
    if hasattr(module, '_auto_quant_state'):
        qstate: AutoQuantizationState = module._auto_quant_state  # type: ignore[assignment]
        for tensor_id, observer in qstate.tensor_id_to_observer.items():
            activation_int8_quantized = \
                observer.dtype in [torch.quint8, torch.qint8]
            if activation_int8_quantized:
                scale, zp = observer.calculate_qparams()
                # tensor_id_to_observer is a ModuleDict which has to have string keys
                # tensor_id_to_scale_zp is a normal dict which can have int keys
                qstate.tensor_id_to_scale_zp[int(tensor_id)] = (scale, zp)
        qstate.tensor_id_to_observer.clear()

    for _, child in module.named_children():
        attach_scale_zp_values_to_model(child)
