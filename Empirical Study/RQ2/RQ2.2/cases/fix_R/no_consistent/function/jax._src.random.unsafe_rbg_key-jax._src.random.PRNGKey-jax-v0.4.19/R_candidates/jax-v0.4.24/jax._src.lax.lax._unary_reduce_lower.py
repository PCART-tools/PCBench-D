def _unary_reduce_lower(reducer, unit_factory, ctx, x, *, axes):
  aval_out, = ctx.avals_out
  dtype = aval_out.dtype
  op = hlo.ReduceOp([mlir.aval_to_ir_type(aval_out)], [x],
                    mlir.ir_constants(unit_factory(aval_out.dtype)),
                    mlir.dense_int_array_v6(axes))
  scalar_type = mlir.aval_to_ir_type(core.ShapedArray((), dtype))
  reducer_region = op.regions[0].blocks.append(scalar_type, scalar_type)
  with ir.InsertionPoint(reducer_region):
    hlo.return_([reducer(*reducer_region.arguments)])
  return op.results
