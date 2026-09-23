def register_quantized_ops(domain: str, version: int):
    # Register all quantized ops
    module = importlib.import_module("torch.onnx.symbolic_caffe2")
    quant_version_ops = inspect.getmembers(module)
    aten_q_ops = {
        "relu",
        "_empty_affine_quantized",
        "dequantize",
        "quantize_per_tensor",
        "upsample_nearest2d",
        "avg_pool2d",
        "reshape",
        "slice",
        "cat",
        "max_pool2d",
        "sigmoid",
    }
    for op, func in quant_version_ops:
        name = f"{domain}::{op}"
        if inspect.isfunction(func) and not registration.registry.is_registered_op(
            name, version
        ):
            if op in aten_q_ops:
                # Override the builtin aten ops
                registration.registry.register(
                    f"aten::{op}", version, func, custom=True
                )
            registration.registry.register(name, version, func)
