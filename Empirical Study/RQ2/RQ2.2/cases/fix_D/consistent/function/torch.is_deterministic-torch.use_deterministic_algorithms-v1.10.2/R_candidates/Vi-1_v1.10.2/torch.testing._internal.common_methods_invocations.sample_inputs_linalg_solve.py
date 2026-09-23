def sample_inputs_linalg_solve(op_info, device, dtype, requires_grad=False, vector_rhs_allowed=True, **kwargs):
    """
    This function generates always solvable input for torch.linalg.solve
    Using random_fullrank_matrix_distinct_singular_value gives a non-singular (=invertible, =solvable) matrices 'a'.
    The first input to torch.linalg.solve is generated as the itertools.product of 'batches' and 'ns'.
    The second input is generated as the product of 'batches', 'ns' and 'nrhs'.
    In total this function generates 18 SampleInputs
    'batches' cases include:
        () - single input,
        (0,) - zero batched dimension,
        (2,) - batch of two matrices.
    'ns' gives 0x0 and 5x5 matrices.
    and 'nrhs' controls the number of vectors to solve for:
        () - using 1 as the number of vectors implicitly
        (1,) - same as () but explicit
        (3,) - solve for 3 vectors.
    Zeros in dimensions are edge cases in the implementation and important to test for in order to avoid unexpected crashes.
    'vector_rhs_allowed' controls whether to include nrhs = () to the list of SampleInputs.
    torch.solve / triangular_solve / cholesky_solve (opposed to torch.linalg.solve) do not allow
    1D tensors (vectors) as the right-hand-side.
    Once torch.solve / triangular_solve / cholesky_solve and its testing are removed,
    'vector_rhs_allowed' may be removed here as well.
    """
    from torch.testing._internal.common_utils import random_fullrank_matrix_distinct_singular_value

    batches = [(), (0, ), (2, )]
    ns = [5, 0]
    if vector_rhs_allowed:
        nrhs = [(), (1,), (3,)]
    else:
        nrhs = [(1,), (3,)]
    out = []
    for n, batch, rhs in product(ns, batches, nrhs):
        a = random_fullrank_matrix_distinct_singular_value(n, *batch, dtype=dtype, device=device)
        a.requires_grad = requires_grad
        b = torch.randn(*batch, n, *rhs, dtype=dtype, device=device)
        b.requires_grad = requires_grad
        out.append(SampleInput(a, args=(b,)))
    return out
