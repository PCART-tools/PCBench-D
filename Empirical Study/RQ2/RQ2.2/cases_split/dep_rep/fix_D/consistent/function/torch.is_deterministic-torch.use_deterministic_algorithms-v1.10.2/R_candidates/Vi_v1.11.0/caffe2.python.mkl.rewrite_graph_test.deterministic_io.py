def deterministic_io(model):
    model = copy.deepcopy(model)
    for i, op in enumerate(model.InitProto().op):
        op.device_option.random_seed = i + 1
    if not model.Proto().external_output:
        model.Proto().external_output.extend([model.Proto().op[-1].output[0]])
    return model
