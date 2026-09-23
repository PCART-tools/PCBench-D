def outputs_are_inputs(outputs, inputs):
    input_ids = {id(inp) for inp in tree_flatten_only(torch.Tensor, inputs)}
    return any(id(out) in input_ids for out in tree_flatten_only(torch.Tensor, outputs))
