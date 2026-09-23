@lu.transformation_with_aux
def _flat_out_axes(leaves, treedef, *args, **kwargs):
  ans = yield args, kwargs
  spec = tree_unflatten(treedef, leaves)
  try:
    spec_flat = tuple(broadcast_prefix(spec, ans, is_leaf=lambda x: x is None))
  except ValueError:
    e, *_ = prefix_errors(spec, ans)
    # TODO(mattjj): currently hardcoded for pmap; generalize to vmap in followup
    msg, = e('pmap out_axes').args
    msg += ("\n\nThe full pytree is the output of the pmapped function. Ensure "
            "that the `out_axes` argument to `pmap` is a pytree prefix of the "
            "pmapped function's output.")
    raise ValueError(msg) from None
  yield ans, spec_flat
