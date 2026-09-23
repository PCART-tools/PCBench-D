def _nary_lower_mhlo(op: Callable, ctx,
                     *args: Union[ir.Value, Sequence[ir.Value]],
                     explicit_type=False, **params):
  """Lowers an elementwise operator to its MHLO/CHLO equivalent.

  Args:
    explicit_type: does the MHLO/CHLO operator require its output type to be
      provided?
  """
  del params
  avals_in, (aval_out,) = ctx.avals_in, ctx.avals_out
  if config.jax_dynamic_shapes:
    substitute = partial(_substitute_axis_sizes_in_aval, ctx.axis_size_env)
    avals_in = map(substitute, avals_in)
    aval_out = substitute(aval_out)
  broadcasted_args = broadcast_mhlo(aval_out, avals_in, args)
  if explicit_type:
    return op(mlir.aval_to_ir_type(aval_out), *broadcasted_args).results
  else:
    return op(*broadcasted_args).results
