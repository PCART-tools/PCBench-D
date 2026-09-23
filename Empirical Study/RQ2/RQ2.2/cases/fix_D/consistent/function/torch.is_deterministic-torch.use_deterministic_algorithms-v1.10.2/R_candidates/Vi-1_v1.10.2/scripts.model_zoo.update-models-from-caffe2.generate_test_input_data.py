def generate_test_input_data(onnx_model, scale):
    real_inputs_names = list(set([input.name for input in onnx_model.graph.input]) - set([init.name for init in onnx_model.graph.initializer]))
    real_inputs = []
    for name in real_inputs_names:
        for input in onnx_model.graph.input:
            if name == input.name:
                real_inputs.append(input)

    test_inputs = []
    for input in real_inputs:
        ndarray = tensortype_to_ndarray(input.type.tensor_type)
        test_inputs.append((input.name, ndarray * scale))

    return test_inputs
