def lstm_backward_setup(lstm_outputs, seed=None):
    hx, _ = lstm_outputs
    return simple_backward_setup(hx, seed)
