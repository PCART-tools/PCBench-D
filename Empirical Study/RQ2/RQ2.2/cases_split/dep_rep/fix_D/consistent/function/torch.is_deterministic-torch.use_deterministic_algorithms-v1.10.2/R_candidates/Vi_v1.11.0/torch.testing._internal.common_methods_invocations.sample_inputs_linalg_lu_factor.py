def sample_inputs_linalg_lu_factor(op_info, device, dtype, requires_grad=False, **kwargs):
    # When calling `lu_factor` we need to assure that the matrix is invertible
    make_fn = make_tensor if "ex" in op_info.name else make_fullrank_matrices_with_distinct_singular_values
    make_arg = partial(make_fn, dtype=dtype, device=device, requires_grad=requires_grad)

    # not needed once OpInfo tests support Iterables
    batch_shapes = ((), (3,), (3, 3))
    # pivot=False only supported in CUDA
    pivots = (True, False) if torch.device(device).type == "cuda" else (True,)
    deltas = (-2, -1, 0, +1, +2)
    for batch_shape, pivot, delta in product(batch_shapes, pivots, deltas):
        shape = batch_shape + (S + delta, S)
        # Insanely annoying that make_fullrank_blablabla accepts a *shape and not a tuple!
        A = make_arg(shape) if "ex" in op_info.name else make_arg(*shape)
        yield SampleInput(A, kwargs={"pivot": pivot})
