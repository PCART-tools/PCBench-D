def _broadcast_translate(op, ctx, avals_in, avals_out, *args):
  """Variant of _standard_translate that performs explicit broadcasting.

  Not all XLA library functions perform their own broadcasting."""
  aval_out, = avals_out
  broadcasted_args = []
  for aval_in, arg in zip(avals_in, args):
    if aval_out.shape != aval_in.shape:
      bcast_dims = tuple(range(len(aval_out.shape) - len(aval_in.shape),
                               len(aval_out.shape)))
      arg = xops.BroadcastInDim(arg, aval_out.shape, bcast_dims)
    broadcasted_args.append(arg)
  return [op(*broadcasted_args)]
