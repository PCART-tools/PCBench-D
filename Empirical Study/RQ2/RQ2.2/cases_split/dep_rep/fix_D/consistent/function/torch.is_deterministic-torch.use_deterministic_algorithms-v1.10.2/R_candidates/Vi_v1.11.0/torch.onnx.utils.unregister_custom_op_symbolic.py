def unregister_custom_op_symbolic(symbolic_name, opset_version):
    ns, op_name = get_ns_op_name_from_custom_op(symbolic_name)
    import torch.onnx.symbolic_registry as sym_registry
    from torch.onnx.symbolic_helper import _onnx_stable_opsets, _onnx_main_opset

    for version in _onnx_stable_opsets + [_onnx_main_opset]:
        if version >= opset_version:
            sym_registry.unregister_op(op_name, ns, version)
