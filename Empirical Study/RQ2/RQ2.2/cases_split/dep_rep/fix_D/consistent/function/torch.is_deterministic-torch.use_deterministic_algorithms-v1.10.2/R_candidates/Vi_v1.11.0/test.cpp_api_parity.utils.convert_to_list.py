def convert_to_list(python_input):
    if isinstance(python_input, torch.Tensor):
        return [python_input]
    else:
        return list(python_input)
