def _dot_general_lowering_rule(
    ctx: LoweringRuleContext, x, y, dimension_numbers, precision, **_
):
  (lhs_dims, rhs_dims), _ = dimension_numbers
  (aval_out,) = ctx.avals_out
  out_type = aval_to_ir_type(aval_out)
  if ctx.avals_out[0].dtype == jnp.float32:
    val = ir.FloatAttr.get(ir.F32Type.get(), 0.0)
  elif ctx.avals_out[0].dtype == jnp.float16:
    val = ir.FloatAttr.get(ir.F16Type.get(), 0.0)
  else:
    raise NotImplementedError(ctx.avals_out[0].dtype)
  if any(len(a.shape) != 2 for a in ctx.avals_in):
    raise NotImplementedError(ctx.avals_in)
  lhs_aval, _ = ctx.avals_in
  # This is really a matrix-vector product. It only looks like matrix-matrix.
  if lhs_dims == (1,) and rhs_dims == (1,) and ctx.avals_in[1].shape[0] == 1:
    if ctx.avals_in[0].shape != ctx.avals_in[1].shape:
      bcast_shape = jnp.broadcast_shapes(
          ctx.avals_in[0].shape, ctx.avals_out[0].shape
      )
      bcast_shape = ir.VectorType.get(
          list(bcast_shape), mlir.dtype_to_ir_type(ctx.avals_out[0].dtype)
      )
      if ctx.avals_in[0].shape != bcast_shape:
        x = vector.BroadcastOp(bcast_shape, x)
      if ctx.avals_in[1].shape != bcast_shape:
        y = vector.BroadcastOp(bcast_shape, y)
    red_type = aval_to_ir_type(lhs_aval.update(shape=(lhs_aval.shape[0],)))
    acc = arith.ConstantOp(
        red_type, ir.DenseElementsAttr.get_splat(red_type, val)
    )
    red = vector.MultiDimReductionOp(
        ir.Attribute.parse("#vector.kind<add>"),
        arith.MulFOp(x, y),
        acc,
        ir.ArrayAttr.get(
            [ir.IntegerAttr.get(ir.IntegerType.get_signless(64), 1)]
        ),
    )
    return vector.ShapeCastOp(out_type, red).result

  if lhs_dims == (1,):
    lhs_dim_attr = ir.Attribute.parse("affine_map<(i, j, k) -> (i, k)>")
  elif lhs_dims == (0,):
    lhs_dim_attr = ir.Attribute.parse("affine_map<(i, j, k) -> (k, i)>")
  if rhs_dims == (0,):
    rhs_dim_attr = ir.Attribute.parse("affine_map<(i, j, k) -> (k, j)>")
  elif rhs_dims == (1,):
    rhs_dim_attr = ir.Attribute.parse("affine_map<(i, j, k) -> (j, k)>")
  out_tile = arith.ConstantOp(
      out_type, ir.DenseElementsAttr.get_splat(out_type, val)
  )
  op = vector.ContractionOp(
      out_type,
      x,
      y,
      out_tile,
      indexing_maps=ir.ArrayAttr.get([
          lhs_dim_attr,
          rhs_dim_attr,
          ir.Attribute.parse("affine_map<(i, j, k) -> (i, j)>"),
      ]),
      iterator_types=ir.ArrayAttr.get([
          ir.Attribute.parse("#vector.iterator_type<parallel>"),
          ir.Attribute.parse("#vector.iterator_type<parallel>"),
          ir.Attribute.parse("#vector.iterator_type<reduction>"),
      ]),
  )
  if precision is not None:
    if precision[0] != precision[1]:
      raise NotImplementedError("Per-operand dot precision unsupported")
    precision = precision[0]
  if precision is None or precision == lax.Precision.DEFAULT:
    pass  # That's the default in Mosaic.
  elif precision == lax.Precision.HIGHEST:
    op.attributes["precision"] = ir.Attribute.parse(
        "#tpu.contract_precision<fp32>"
    )
  else:
    raise NotImplementedError(f"Unsupported dot precision: {precision}")
  return op.result
