def index_variable(shape, max_indices, device=torch.device('cpu')):
    if not isinstance(shape, tuple):
        shape = (shape,)
    index = torch.rand(*shape, dtype=torch.double, device=device).mul_(max_indices).floor_().long()
    return index
