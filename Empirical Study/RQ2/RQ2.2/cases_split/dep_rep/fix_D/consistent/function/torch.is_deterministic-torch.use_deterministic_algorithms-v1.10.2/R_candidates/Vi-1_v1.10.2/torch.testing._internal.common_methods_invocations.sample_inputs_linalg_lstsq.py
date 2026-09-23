def sample_inputs_linalg_lstsq(op_info, device, dtype, requires_grad=False, **kwargs):
    from torch.testing._internal.common_utils import random_well_conditioned_matrix
    out = []
    for batch in ((), (3,), (3, 3)):
        shape = batch + (3, 3)
        # NOTE: inputs are not marked with `requires_grad` since
        # linalg_lstsq is not differentiable
        a = random_well_conditioned_matrix(*shape, dtype=dtype, device=device)
        b = make_tensor(shape, device, dtype, low=None, high=None)
        out.append(SampleInput(a, args=(b,)))
    return out
