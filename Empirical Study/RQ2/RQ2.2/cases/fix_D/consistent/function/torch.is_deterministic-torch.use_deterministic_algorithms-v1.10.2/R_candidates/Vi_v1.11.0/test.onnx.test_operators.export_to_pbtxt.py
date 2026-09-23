def export_to_pbtxt(model, inputs, *args, **kwargs):
    return torch.onnx.export_to_pretty_string(
        model, inputs, google_printer=True, *args, **kwargs)
