def create_constant(network, tensor, name, dtype):
    if isinstance(tensor, int):
        tensor = torch.IntTensor([tensor])

    if isinstance(tensor, float):
        tensor = torch.Tensor([tensor])

    if dtype:
        tensor = tensor.to(dtype)

    constant = network.add_constant(tensor.shape, to_numpy(tensor))
    constant.name = name
    return constant.get_output(0)
