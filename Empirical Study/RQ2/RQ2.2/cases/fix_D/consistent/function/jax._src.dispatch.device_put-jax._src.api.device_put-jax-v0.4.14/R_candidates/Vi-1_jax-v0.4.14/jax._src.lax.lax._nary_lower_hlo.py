def _nary_lower_hlo(op: Callable, ctx,
                    *args: Union[ir.Value, Sequence[ir.Value]],
                    explicit_type=False, **params):
  """Lowers an elementwise operator to its MLIR equivalent.

  Args:
    explicit_type: does the MLIR op require its output type to be provided?
  """
  del params
  avals_in, (aval_out,) = ctx.avals_in, ctx.avals_out
  broadcasted_args = mlir.multi_broadcast_in_dim(
      ctx, args, avals_in, aval_out.shape)

  if explicit_type:
    return op(mlir.aval_to_ir_type(aval_out), *broadcasted_args).results
  else:
    return op(*broadcasted_args).results
