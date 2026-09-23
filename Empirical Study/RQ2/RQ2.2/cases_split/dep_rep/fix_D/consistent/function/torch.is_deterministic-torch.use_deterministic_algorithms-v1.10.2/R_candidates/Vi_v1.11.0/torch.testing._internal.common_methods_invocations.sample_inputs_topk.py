def sample_inputs_topk(op_info, device, dtype, requires_grad, **kwargs):
    def get_tensor_input(size):
        return make_tensor(size, device, dtype, requires_grad=requires_grad)

    inputs = []
    inputs.append(SampleInput(get_tensor_input((S, M, S)), args=(3,)))
    inputs.append(SampleInput(get_tensor_input((S, M, S)), args=(3, 1)))
    inputs.append(SampleInput(get_tensor_input((S, M, S)), args=(3, -2)))
    inputs.append(SampleInput(get_tensor_input((S, M, S)), args=(3, 1, True)))
    inputs.append(SampleInput(get_tensor_input((S, M, S)), args=(3, -2, True)))
    inputs.append(SampleInput(get_tensor_input((S, M, S)), args=(3, 1, True, True)))
    inputs.append(SampleInput(get_tensor_input((S, M, S)), args=(3, -2, True, True)))

    inputs.append(SampleInput(get_tensor_input(()), args=(1,)))
    inputs.append(SampleInput(get_tensor_input(()), args=(1, 0)))
    inputs.append(SampleInput(get_tensor_input(()), args=(1, -1)))
    inputs.append(SampleInput(get_tensor_input(()), args=(1, 0, True)))
    inputs.append(SampleInput(get_tensor_input(()), args=(1, -1, True)))
    inputs.append(SampleInput(get_tensor_input(()), args=(1, 0, True, True)))
    inputs.append(SampleInput(get_tensor_input(()), args=(1, -1, True, True)))

    return inputs
