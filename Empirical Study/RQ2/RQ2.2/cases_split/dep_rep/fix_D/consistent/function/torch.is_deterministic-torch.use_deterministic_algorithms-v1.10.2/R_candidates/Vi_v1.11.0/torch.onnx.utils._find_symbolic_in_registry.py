def _find_symbolic_in_registry(domain, op_name, opset_version, operator_export_type):
    import torch.onnx.symbolic_registry as sym_registry
    if not sym_registry.is_registered_op(op_name, domain, opset_version):
        if operator_export_type == OperatorExportTypes.ONNX_FALLTHROUGH:
            # Use the original node directly
            return None
    return sym_registry.get_registered_op(op_name, domain, opset_version)
