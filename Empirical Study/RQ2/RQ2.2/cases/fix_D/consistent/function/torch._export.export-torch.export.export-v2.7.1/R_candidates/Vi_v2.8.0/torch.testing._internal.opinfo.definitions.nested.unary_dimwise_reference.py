def unary_dimwise_reference(op, sample, batchwise_reference=None):
    # extract info about the dim args this op supports
    assert op._extra_op_data.dim_args is not None
    single_dim_argname, dimlist_argname = op._extra_op_data.get_dim_argnames()
    # only support a single non-list dim arg for now
    assert dimlist_argname is None
    assert single_dim_argname is not None
    if sample.kwargs[single_dim_argname] == 0:
        # unbind reference won't work for batch-wise operation; handle this case here
        assert batchwise_reference is not None
        return batchwise_reference(op, sample)
    return unbind_reference(op, sample)
