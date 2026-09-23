def varlen_lstm_creator(script=False, **kwargs):
    sequences, _, hidden, params, _ = varlen_lstm_inputs(
        return_module=False, **kwargs)
    inputs = [sequences, hidden] + params[0]
    return ModelDef(
        inputs=inputs,
        params=flatten_list(params),
        forward=varlen_lstm_factory(lstm_cell, script),
        backward_setup=varlen_lstm_backward_setup,
        backward=simple_backward)
