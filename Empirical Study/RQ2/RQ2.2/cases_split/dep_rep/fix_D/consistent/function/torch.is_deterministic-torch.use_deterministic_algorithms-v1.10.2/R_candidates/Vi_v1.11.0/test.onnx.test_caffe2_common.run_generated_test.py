def run_generated_test(model_file, data_dir, device="CPU"):
    model = onnx.load(model_file)
    input_num = len(glob.glob(os.path.join(data_dir, "input_*.pb")))
    inputs = []
    for i in range(input_num):
        inputs.append(numpy_helper.to_array(load_tensor_as_numpy_array(
            os.path.join(data_dir, "input_{}.pb".format(i)))))
    output_num = len(glob.glob(os.path.join(data_dir, "output_*.pb")))
    outputs = []
    for i in range(output_num):
        outputs.append(numpy_helper.to_array(load_tensor_as_numpy_array(
            os.path.join(data_dir, "output_{}.pb".format(i)))))
    prepared = c2.prepare(model, device=device)
    c2_outputs = prepared.run(inputs)
    assert_similar(outputs, c2_outputs)
