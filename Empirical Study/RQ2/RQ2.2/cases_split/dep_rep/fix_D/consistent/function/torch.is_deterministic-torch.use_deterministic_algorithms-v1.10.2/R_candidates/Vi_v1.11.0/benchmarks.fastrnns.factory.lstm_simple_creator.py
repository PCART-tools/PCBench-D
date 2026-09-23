def lstm_simple_creator(script=True, **kwargs):
    input, hidden, params, _ = lstm_inputs(return_module=False, **kwargs)
    inputs = [input] + [h[0] for h in hidden] + params[0]
    return ModelDef(
        inputs=inputs,
        params=flatten_list(params),
        forward=lstm_factory_simple(flat_lstm_cell, script),
        backward_setup=lstm_backward_setup,
        backward=simple_backward)
