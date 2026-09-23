def stack(tensors: list[list[int]], dim: int):
    unsqueezed_tensors: list[list[int]] = []
    for tensor in tensors:
        unsqueezed = unsqueeze(tensor, dim)
        unsqueezed_tensors.append(unsqueezed)
    return cat(unsqueezed_tensors, dim)
