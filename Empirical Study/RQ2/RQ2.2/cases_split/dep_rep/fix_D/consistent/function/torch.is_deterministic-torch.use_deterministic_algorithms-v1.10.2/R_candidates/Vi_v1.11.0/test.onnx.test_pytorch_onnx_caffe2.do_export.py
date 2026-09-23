def do_export(model, inputs, *args, **kwargs):
    f = io.BytesIO()
    out = torch.onnx._export(model, inputs, f, *args, **kwargs)
    if isinstance(model, torch.jit.ScriptModule):
        # Special case for common case of passing a single Tensor
        if isinstance(inputs, torch.Tensor):
            inputs = (inputs,)
        out = model(*inputs)
    return f.getvalue(), out
