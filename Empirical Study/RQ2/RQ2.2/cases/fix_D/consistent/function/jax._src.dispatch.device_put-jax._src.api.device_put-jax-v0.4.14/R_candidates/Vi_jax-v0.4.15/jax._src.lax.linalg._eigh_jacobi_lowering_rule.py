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
  result_types = [eigvecs_type, eigvals_type]

  backend_config = f"{int(lower)},{int(sort_eigenvalues)},100,1e-6"

  if any(not is_constant_shape(aval_out.shape)
         for aval_out in ctx.avals_out):
    result_shapes = [
        mlir.eval_dynamic_shape_as_tensor(ctx, aval_out.shape)
        # The custom call returns the results swapped
        for aval_out in list(reversed(ctx.avals_out))
    ]
  else:
    result_shapes = None
  op = mlir.custom_call(
      "Eigh",
      result_types=result_types,
      operands=[operand],
      backend_config=backend_config,
      api_version=1,
      result_shapes=result_shapes,
  )
  return op.results[1], op.results[0]
