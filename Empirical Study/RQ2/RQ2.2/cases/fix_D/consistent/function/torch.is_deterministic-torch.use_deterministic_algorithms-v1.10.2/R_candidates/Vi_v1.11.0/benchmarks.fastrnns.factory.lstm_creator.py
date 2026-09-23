def lstm_creator(script=True, **kwargs):
    input, hidden, params, _ = lstm_inputs(return_module=False, **kwargs)
    inputs = [input, hidden] + params[0]
    return ModelDef(
        inputs=inputs,
        params=flatten_list(params),
        forward=lstm_factory(lstm_cell, script),
        backward_setup=lstm_backward_setup,
        backward=simple_backward)
