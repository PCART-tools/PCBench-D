def _cmp_lowering_rule(prim, ctx: LoweringRuleContext, x, y):
  x_aval, y_aval = ctx.avals_in
  x_dtype, y_dtype = x_aval.dtype, y_aval.dtype
  if isinstance(y, (np.generic, np.ndarray, int, float)):
    y = ir_constant(y, mlir_type=mlir.dtype_to_ir_type(y_dtype))
  if isinstance(x, (np.generic, np.ndarray, int, float)):
    x = ir_constant(x, mlir_type=mlir.dtype_to_ir_type(x_dtype))
  bcast_shape = np.broadcast_shapes(x_aval.shape, y_aval.shape)
  if x_aval.shape != bcast_shape:
    bcast_shape = ir.VectorType.get(
        list(bcast_shape), mlir.dtype_to_ir_type(x_aval.dtype)
    )
    x = vector.BroadcastOp(bcast_shape, x).result
  if y_aval.shape != bcast_shape:
    bcast_shape = ir.VectorType.get(
        list(bcast_shape), mlir.dtype_to_ir_type(y_aval.dtype)
    )
    y = vector.BroadcastOp(bcast_shape, y).result
  if jnp.issubdtype(x_dtype, jnp.integer) and jnp.issubdtype(
      y_dtype, jnp.integer
  ):
    pred = _cmpi_lowering_types[prim]
    predicate = ir.IntegerAttr.get(ir.IntegerType.get_signless(64), pred)
    return arith.CmpIOp(predicate, x, y).result
  elif jnp.issubdtype(x_dtype, jnp.floating) and jnp.issubdtype(
      y_dtype, jnp.floating
  ):
    pred = _cmpf_lowering_types[prim]
    predicate = ir.IntegerAttr.get(ir.IntegerType.get_signless(64), pred)
    return arith.CmpFOp(predicate, x, y).result
  raise NotImplementedError((x_dtype, y_dtype))
