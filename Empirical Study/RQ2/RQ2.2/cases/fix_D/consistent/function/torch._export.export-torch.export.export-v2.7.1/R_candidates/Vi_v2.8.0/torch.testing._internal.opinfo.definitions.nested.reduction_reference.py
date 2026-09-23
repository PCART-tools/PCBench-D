def reduction_reference(op, sample):
    assert sample.input.is_nested

    # extract info about the dim args this op supports
    assert op._extra_op_data.dim_args is not None
    single_dim_argname, dimlist_argname = op._extra_op_data.get_dim_argnames()
    assert single_dim_argname is not None

    dim = sample.kwargs.get(
        dimlist_argname, sample.kwargs.get(single_dim_argname, None)
    )
    keepdim = sample.kwargs.get("keepdim", False)
    assert dim != 0, "reductions over just the batch dim are not supported"
    if isinstance(dim, (tuple, list)):
        reduce_on_ragged = sample.input._ragged_idx in dim
        reduce_on_batch = 0 in dim
    else:
        reduce_on_ragged = sample.input._ragged_idx == dim
        reduce_on_batch = dim == 0

    if dim is None:
        # calculate reference value by running reduction on values buffer
        return op.op(sample.input.values(), *sample.args, **sample.kwargs)

    if reduce_on_ragged and reduce_on_batch:
        # run reference directly on buffer with dims converted to inner space
        from torch.nested._internal.ops import _outer_to_inner_dim

        ref_kwargs = dict(sample.kwargs)
        assert dimlist_argname is not None
        ref_kwargs[dimlist_argname] = _outer_to_inner_dim(
            sample.input.dim(), dim, sample.input._ragged_idx, canonicalize=True
        )
        out = op.op(sample.input.values(), *sample.args, **ref_kwargs)
        if keepdim:
            if isinstance(out, (tuple, list)):
                # some ops return multiple things; unsqueeze all of them
                out = type(out)(o.unsqueeze(0) for o in out)
            else:
                out = out.unsqueeze(0)
        return out

    if reduce_on_ragged and not reduce_on_batch:
        # calculate reference value by running an unbind reference and stacking
        out_ref_components = unbind_reference(op, sample, wrap_output_as_njt=False)
        if len(out_ref_components) > 0 and isinstance(
            out_ref_components[0], (tuple, list)
        ):
            # some ops return multiple things; stack all of them
            num_returns = len(out_ref_components[0])
            # ensure we get the same number of returns for each invocation
            assert all(len(o) == num_returns for o in out_ref_components)
            # stack same index returns from each invocation
            stacked_returns = [
                torch.stack([o[r] for o in out_ref_components], dim=0)
                for r in range(num_returns)
            ]
            return type(out_ref_components[0])(stacked_returns)
        return torch.stack(out_ref_components, dim=0)

    # unbind reference works for other reductions
    return unbind_reference(op, sample)
