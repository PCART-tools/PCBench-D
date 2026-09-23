@wraps(np.einsum)
def einsum(*operands, **kwargs):
    casting = kwargs.pop('casting', 'safe')
    dtype = kwargs.pop('dtype', None)
    optimize = kwargs.pop('optimize', False)
    order = kwargs.pop('order', 'K')
    split_every = kwargs.pop('split_every', None)
    if kwargs:
        raise TypeError("einsum() got unexpected keyword "
                        "argument(s) %s" % ",".join(kwargs))

    einsum_dtype = dtype

    inputs, outputs, ops = parse_einsum_input(operands)
    subscripts = '->'.join((inputs, outputs))

    # Infer the output dtype from operands
    if dtype is None:
        dtype = np.result_type(*[o.dtype for o in ops])

    if einsum_can_optimize:
        if optimize is not False:
            # Avoid computation of dask arrays within np.einsum_path
            # by passing in small numpy arrays broadcasted
            # up to the right shape
            fake_ops = [np.broadcast_to(o.dtype.type(0), shape=o.shape)
                        for o in ops]
            optimize, _ = np.einsum_path(subscripts, *fake_ops,
                                         optimize=optimize)
        kwargs = {'optimize': optimize}
    else:
        kwargs = {}

    inputs = [tuple(i) for i in inputs.split(",")]

    # Set of all indices
    all_inds = set(a for i in inputs for a in i)

    # Which indices are contracted?
    contract_inds = all_inds - set(outputs)
    ncontract_inds = len(contract_inds)

    # Introduce the contracted indices into the atop product
    # so that we get numpy arrays, not lists
    result = atop(chunk.einsum, tuple(outputs) + tuple(contract_inds),
                  *(a for ap in zip(ops, inputs) for a in ap),
                  # atop parameters
                  adjust_chunks={ind: 1 for ind in contract_inds}, dtype=dtype,
                  # np.einsum parameters
                  subscripts=subscripts, kernel_dtype=einsum_dtype,
                  ncontract_inds=ncontract_inds, order=order,
                  casting=casting, **kwargs)

    # Now reduce over any extra contraction dimensions
    if ncontract_inds > 0:
        size = len(outputs)
        return result.sum(axis=list(range(size, size + ncontract_inds)),
                          split_every=split_every)

    return result
