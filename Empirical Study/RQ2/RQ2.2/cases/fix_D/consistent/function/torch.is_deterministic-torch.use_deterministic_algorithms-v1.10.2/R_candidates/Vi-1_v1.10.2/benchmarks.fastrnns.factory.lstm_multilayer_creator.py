def lstm_multilayer_creator(script=True, **kwargs):
    input, hidden, params, _ = lstm_inputs(return_module=False, **kwargs)
    inputs = [input, hidden, flatten_list(params)]
    return ModelDef(
        inputs=inputs,
        params=flatten_list(params),
        forward=lstm_factory_multilayer(lstm_cell, script),
        backward_setup=lstm_backward_setup,
        backward=simple_backward)
