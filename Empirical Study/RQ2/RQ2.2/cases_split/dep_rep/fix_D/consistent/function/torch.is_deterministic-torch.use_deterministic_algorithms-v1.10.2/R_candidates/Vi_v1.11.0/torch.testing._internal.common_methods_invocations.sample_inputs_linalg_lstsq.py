def sample_inputs_linalg_lstsq(op_info, device, dtype, requires_grad=False, **kwargs):
    from torch.testing._internal.common_utils import random_well_conditioned_matrix

    device = torch.device(device)

    drivers: Tuple[str, ...]
    if device.type == 'cuda':
        drivers = ('gels',)
    else:
        drivers = ('gels', 'gelsy', 'gelss', 'gelsd')

    # we generate matrices of shape (..., n + delta, n)
    deltas: Tuple[int, ...]
    if device.type == 'cpu' or has_cusolver():
        deltas = (-1, 0, +1)
    # only square systems if Cusolver is not available
    # becase we solve a lstsq problem with a transposed matrix in the backward
    else:
        deltas = (0,)

    out = []
    for batch, driver, delta in product(((), (3,), (3, 3)), drivers, deltas):
        shape = batch + (3 + delta, 3)
        a = random_well_conditioned_matrix(*shape, dtype=dtype, device=device)
        a.requires_grad_(requires_grad)
        b = make_tensor(shape, device, dtype, low=None, high=None, requires_grad=requires_grad)
        out.append(SampleInput(a, args=(b,), kwargs=dict(driver=driver)))
    return out
