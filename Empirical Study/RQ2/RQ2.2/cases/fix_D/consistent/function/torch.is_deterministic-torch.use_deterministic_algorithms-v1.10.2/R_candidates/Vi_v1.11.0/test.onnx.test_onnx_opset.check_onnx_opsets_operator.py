def check_onnx_opsets_operator(module, x, ops, opset_versions, training=torch.onnx.TrainingMode.EVAL,
                               input_names=None, dynamic_axes=None):
    for opset_version in opset_versions:
        f = io.BytesIO()
        torch.onnx.export(module, x, f,
                          opset_version=opset_version,
                          training=training,
                          input_names=input_names,
                          dynamic_axes=dynamic_axes)
        model = onnx.load(io.BytesIO(f.getvalue()))
        check_onnx_opset_operator(model, ops[opset_version], opset_version)
