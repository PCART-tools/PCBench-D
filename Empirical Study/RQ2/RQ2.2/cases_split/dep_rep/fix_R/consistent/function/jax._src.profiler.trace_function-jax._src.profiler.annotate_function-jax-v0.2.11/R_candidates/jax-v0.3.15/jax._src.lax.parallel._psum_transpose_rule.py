def _psum_transpose_rule(cts, *args, axes, axis_index_groups):
  named_axes, pos_axes = axes_partition = [], []
  for axis in axes:
    axes_partition[isinstance(axis, int)].append(axis)

  if pos_axes:
    def broadcast_positional(ct, arg):
      assert ad.is_undefined_primal(arg)
      if type(ct) is ad.Zero: return ad.Zero(arg.aval)
      return lax._reduce_sum_transpose_rule(ct, arg, axes=pos_axes)[0]
    cts = map(broadcast_positional, cts, args)

  # We treat psum as psum + pbroadcast, which is why the transpose reduces
  # over the named axes again (unlike for positional axes).
  nonzero_out_cts, treedef = tree_util.tree_flatten(cts)
  nonzero_in_cts = psum_p.bind(*nonzero_out_cts, axes=tuple(named_axes),
                               axis_index_groups=axis_index_groups)
  return tree_util.tree_unflatten(treedef, nonzero_in_cts)
