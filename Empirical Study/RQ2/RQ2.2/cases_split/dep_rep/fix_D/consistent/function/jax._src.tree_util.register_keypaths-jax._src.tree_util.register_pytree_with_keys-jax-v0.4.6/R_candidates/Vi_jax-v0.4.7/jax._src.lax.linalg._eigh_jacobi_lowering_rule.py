def _eigh_jacobi_lowering_rule(ctx, operand, lower, sort_eigenvalues):
  operand_aval, = ctx.avals_in
  if operand_aval.shape[-1] == 0:
    reshape_aval = operand_aval.update(shape=operand_aval.shape[:-1])
    return [
        hlo.RealOp(mlir.reshape(ctx, operand, reshape_aval)).result,
        operand,
    ]

  eigvals_type = mlir.aval_to_ir_type(ctx.avals_out[0])
  eigvecs_type = mlir.aval_to_ir_type(ctx.avals_out[1])
  eigh_type = ir.TupleType.get_tuple([eigvecs_type, eigvals_type])

  backend_config = f"{int(lower)},{int(sort_eigenvalues)},100,1e-6"
  op = hlo.CustomCallOp(
      [eigh_type],
      [operand],
      call_target_name=ir.StringAttr.get("Eigh"),
      has_side_effect=ir.BoolAttr.get(False),
      backend_config=ir.StringAttr.get(backend_config),
      api_version=mlir.i32_attr(1),
  )
  return (
      hlo.GetTupleElementOp(op, 1).result,
      hlo.GetTupleElementOp(op, 0).result,
  )
