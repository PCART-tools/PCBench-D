def sample_inputs_unary_dimwise(
    op_info, device, dtype, requires_grad, op_kwargs=None, **kwargs
):
    if op_kwargs is None:
        op_kwargs = {}

    # only support a single non-list dim arg for now
    assert op_info._extra_op_data is not None
    single_dim_argname, dimlist_argname = op_info._extra_op_data.get_dim_argnames()
    assert single_dim_argname is not None
    assert dimlist_argname is None

    for njt in _sample_njts(
        device=device, dtype=dtype, requires_grad=requires_grad, dims=[2, 3, 4]
    ):
        for dim in range(njt.dim()):
            kwargs = {single_dim_argname: dim}
            kwargs.update(op_kwargs)
            yield SampleInput(
                _clone(njt),
                kwargs=kwargs,
                name=f"{_describe_njt(njt)}: {_describe_dim(njt, dim)}",
            )
