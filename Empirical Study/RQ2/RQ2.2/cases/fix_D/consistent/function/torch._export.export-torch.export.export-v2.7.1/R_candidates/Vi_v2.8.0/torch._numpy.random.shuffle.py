@deco_stream
def shuffle(x):
    # no @normalizer because we do not cast e.g. lists to tensors
    from ._ndarray import ndarray

    if isinstance(x, torch.Tensor):
        tensor = x
    elif isinstance(x, ndarray):
        tensor = x.tensor
    else:
        raise NotImplementedError("We do not random.shuffle lists in-place")

    perm = torch.randperm(tensor.shape[0])
    xp = tensor[perm]
    tensor.copy_(xp)
