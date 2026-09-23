def _check_error(error, *, debug=False):
  if any(map(np.shape, error._pred.values())):
    error = _reduce_any_error(error)
  err_args, tree_def = tree_flatten(error)

  return check_p.bind(*err_args, err_tree=tree_def, debug=debug)
