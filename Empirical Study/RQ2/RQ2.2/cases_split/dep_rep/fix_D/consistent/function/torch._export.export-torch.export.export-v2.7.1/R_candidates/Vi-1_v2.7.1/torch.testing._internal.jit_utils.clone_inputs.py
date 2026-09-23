def clone_inputs(args):
    inputs: list[Union[torch.Tensor, list[torch.Tensor]]] = []

    for arg in args:
        if isinstance(arg, torch.Tensor):
            inputs.append(arg.detach().clone())
        elif is_iterable_of_tensors(arg):
            inputs.append([t.detach().clone() for t in arg])
        else:
            inputs.append(arg)

    return inputs
