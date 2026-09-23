def onnx_verify(onnx_model, inputs, ref_outputs):
    prepared = caffe2.python.onnx.backend.prepare(onnx_model)
    onnx_inputs = []
    for input in inputs:
        if isinstance(input, tuple):
            onnx_inputs.append(input[1])
        else:
            onnx_inputs.append(input)
    onnx_outputs = prepared.run(inputs=onnx_inputs)
    np.testing.assert_almost_equal(onnx_outputs, ref_outputs, decimal=3)
