def GetLSTMParamNames():
    weight_params = ["input_gate_w", "forget_gate_w", "output_gate_w", "cell_w"]
    bias_params = ["input_gate_b", "forget_gate_b", "output_gate_b", "cell_b"]
    return {'weights': weight_params, 'biases': bias_params}
