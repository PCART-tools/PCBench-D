def export_to_pbtxt(model, inputs, *args, **kwargs):
    return torch.onnx.export_to_pretty_string(
        model, inputs, None, verbose=False, google_printer=True,
        *args, **kwargs)
