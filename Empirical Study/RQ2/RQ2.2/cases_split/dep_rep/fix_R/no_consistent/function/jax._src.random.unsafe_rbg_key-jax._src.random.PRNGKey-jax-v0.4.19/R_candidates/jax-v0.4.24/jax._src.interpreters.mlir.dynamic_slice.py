def dynamic_slice(ctx: LoweringRuleContext, aval_out, x, *,
                  start_indices) -> ir.Value:
  x_aval = ctx.avals_in[0]
  if dtypes.issubdtype(aval_out.dtype, dtypes.extended):
    elt_shape = aval_out.dtype._rules.physical_element_aval(
        aval_out.dtype).shape
    index_avals = ctx.avals_in[1:]
    dtype = dtypes.canonicalize_dtype(
        index_avals[0].dtype if index_avals else 'int64')  # type: ignore
    trailing_zeros = [ir_constant(np.array(0, dtype))] * len(elt_shape)
    start_indices = (*start_indices, *trailing_zeros)
    aval_out = core.physical_aval(aval_out)
    x_aval = core.physical_aval(x_aval)

  slice_sizes = aval_out.shape
  if not core.is_constant_shape(slice_sizes):
    # lax.dynamic_slice clamps the start indices, but we are going to
    # lower to RealDynamicSliceOp, which is a version of SliceOp, and does
    # not have the clamping behavior. We clamp start ourselves.
    slice_sizes = eval_dynamic_shape_as_tensor(ctx, slice_sizes)
    clamped_start = hlo.clamp(
      shape_tensor([0] * len(start_indices)),
      shape_tensor(start_indices),
      hlo.subtract(
        eval_dynamic_shape_as_tensor(ctx, x_aval.shape),  # type: ignore
        slice_sizes))
    return hlo.real_dynamic_slice(
        aval_to_ir_type(aval_out), x,
        clamped_start,
        hlo.add(clamped_start, slice_sizes),
        shape_tensor([1] * len(start_indices))
    )
  else:
    return hlo.dynamic_slice(x, start_indices, dense_int_array(slice_sizes))
