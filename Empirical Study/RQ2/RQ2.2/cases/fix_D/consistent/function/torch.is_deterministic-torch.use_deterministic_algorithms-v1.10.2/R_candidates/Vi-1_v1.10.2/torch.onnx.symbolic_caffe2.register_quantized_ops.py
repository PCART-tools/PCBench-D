def register_quantized_ops(domain, version):
    # Register all the non-quantized ops
    sym_registry.register_version("", version)
    # Register all quantized ops
    module = importlib.import_module("torch.onnx.symbolic_caffe2")
    sym_registry._symbolic_versions["caffe2"] = module
    quant_version_ops = getmembers(sym_registry._symbolic_versions["caffe2"])
    for op in quant_version_ops:
        if isfunction(op[1]) and not sym_registry.is_registered_op(op[0], domain, version):
            aten_q_ops = ["relu", "_empty_affine_quantized", "dequantize",
                          "quantize_per_tensor", "upsample_nearest2d", "avg_pool2d",
                          "reshape", "slice", "cat", "max_pool2d", "sigmoid"]
            if op[0] in aten_q_ops:
                sym_registry.register_op(op[0], op[1], "", version)
            sym_registry.register_op(op[0], op[1], domain, version)
