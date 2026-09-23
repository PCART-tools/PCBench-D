def attach_op_convert_info_to_model(
    module: torch.nn.Module,
) -> None:
    """
    Calculates the info needed to convert each op and attaches
    it to the parent module. This is done to avoid recalculating these values
    at inference.
    """
    if hasattr(module, '_auto_quant_state'):
        qstate: AutoQuantizationState = module._auto_quant_state  # type: ignore[assignment]
        for _, seen_op_info in qstate.idx_to_seen_op_infos.items():
            qstate.idx_to_op_convert_info[seen_op_info.idx] = \
                qstate.calculate_op_convert_info(seen_op_info)

    for _, child in module.named_children():
        attach_op_convert_info_to_model(child)
