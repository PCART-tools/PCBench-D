def dynamic_update_slice(ctx: LoweringRuleContext, aval_out, x, update, *,
                         start_indices) -> ir.Value:
  if dtypes.issubdtype(aval_out.dtype, dtypes.extended):
    elt_shape = aval_out.dtype._rules.physical_element_aval(
        aval_out.dtype).shape
    index_avals = ctx.avals_in[2:]
    dtype = dtypes.canonicalize_dtype(
        index_avals[0].dtype if index_avals else 'int64')  # type: ignore
    zeros = [ir_constant(np.array(0, dtype=dtype))] * len(elt_shape)
    start_indices = (*start_indices, *zeros)
    physical_aval_out = core.physical_aval(aval_out)
    return dynamic_update_slice(ctx, physical_aval_out, x, update,
                                start_indices=start_indices)
  else:
    # TODO(necula): handle dynamic shapes
    return hlo.DynamicUpdateSliceOp(x, update, start_indices).result
