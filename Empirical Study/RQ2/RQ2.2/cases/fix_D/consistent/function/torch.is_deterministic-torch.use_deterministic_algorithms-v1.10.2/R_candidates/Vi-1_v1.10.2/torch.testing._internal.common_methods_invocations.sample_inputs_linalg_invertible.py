def sample_inputs_linalg_invertible(op_info, device, dtype, requires_grad=False, **kwargs):
    """
    This function generates always invertible input for linear algebra ops using
    random_fullrank_matrix_distinct_singular_value.
    The input is generated as the itertools.product of 'batches' and 'ns'.
    In total this function generates 8 SampleInputs
    'batches' cases include:
        () - single input,
        (0,) - zero batched dimension,
        (2,) - batch of two matrices,
        (1, 1) - 1x1 batch of matrices
    'ns' gives 0x0 and 5x5 matrices.
    Zeros in dimensions are edge cases in the implementation and important to test for in order to avoid unexpected crashes.
    """
    from torch.testing._internal.common_utils import random_fullrank_matrix_distinct_singular_value

    batches = [(), (0, ), (2, ), (1, 1)]
    ns = [5, 0]
    out = []
    for batch, n in product(batches, ns):
        a = random_fullrank_matrix_distinct_singular_value(n, *batch, dtype=dtype, device=device)
        a.requires_grad = requires_grad
        out.append(SampleInput(a))
    return out
