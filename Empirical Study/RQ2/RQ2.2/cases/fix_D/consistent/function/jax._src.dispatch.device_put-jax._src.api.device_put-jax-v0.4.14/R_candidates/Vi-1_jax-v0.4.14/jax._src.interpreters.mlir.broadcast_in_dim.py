def broadcast_in_dim(ctx: LoweringRuleContext, op, aval_out: core.AbstractValue, *,
                     broadcast_dimensions) -> ir.Value:
  # broadcast_dimension[i] is the axis of the result where the axis i of
  # op is broadcast.
  # Lower a possibly-dynamic broadcast_in_dim
  if dtypes.issubdtype(aval_out.dtype, dtypes.extended):  # type: ignore
    elt_shape = aval_out.dtype._rules.physical_element_aval(  # type: ignore
        aval_out.dtype).shape                                 # type: ignore
    trailing_dims = [aval_out.ndim + i for i in range(len(elt_shape))]  # type: ignore
    broadcast_dimensions = [*broadcast_dimensions, *trailing_dims]
    physical_aval_out = core.physical_aval(aval_out)
    return broadcast_in_dim(
        ctx, op, physical_aval_out, broadcast_dimensions=broadcast_dimensions)
  else:
    if not core.is_constant_shape(aval_out.shape):  # type: ignore
      shape = eval_dynamic_shape_as_tensor(ctx, aval_out.shape)  # type: ignore
      return hlo.DynamicBroadcastInDimOp(
          aval_to_ir_type(aval_out), op,
          shape,
          dense_int_elements(broadcast_dimensions),
      ).result
    else:
      assert all(d != ir.ShapedType.get_dynamic_size()
                 for d in aval_out.shape), aval_out  # type: ignore
      return hlo.BroadcastInDimOp(
          aval_to_ir_type(aval_out), op,
          dense_int_elements(broadcast_dimensions)).result
