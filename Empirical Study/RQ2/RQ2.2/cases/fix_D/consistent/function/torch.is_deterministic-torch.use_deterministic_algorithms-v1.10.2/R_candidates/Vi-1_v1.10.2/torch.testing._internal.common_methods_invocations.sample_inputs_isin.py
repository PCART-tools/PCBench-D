def sample_inputs_isin(op_info, device, dtype, requires_grad):
    element = make_tensor((L,), device, dtype, low=None, high=None, requires_grad=requires_grad)
    indices = torch.randint(0, L, size=[S])
    test_elements = element[indices].clone()
    return [
        SampleInput(element, args=(test_elements,))
    ]
