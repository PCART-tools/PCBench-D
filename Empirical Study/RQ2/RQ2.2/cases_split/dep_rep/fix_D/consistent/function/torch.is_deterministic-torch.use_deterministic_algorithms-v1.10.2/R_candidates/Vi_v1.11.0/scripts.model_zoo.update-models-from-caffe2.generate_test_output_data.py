def generate_test_output_data(caffe2_init_net, caffe2_predict_net, inputs):
    p = c2_workspace.Predictor(caffe2_init_net, caffe2_predict_net)
    inputs_map = {input[0]:input[1] for input in inputs}

    output = p.run(inputs_map)
    c2_workspace.ResetWorkspace()
    return output
