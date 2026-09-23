def get_inputs_from_args_and_kwargs(args, kwargs, input_names):
    inputs = []
    for i, key in enumerate(input_names):
        if key not in kwargs:
            inputs.append(args[i])
        else:
            inputs.append(kwargs[key])
    return inputs
