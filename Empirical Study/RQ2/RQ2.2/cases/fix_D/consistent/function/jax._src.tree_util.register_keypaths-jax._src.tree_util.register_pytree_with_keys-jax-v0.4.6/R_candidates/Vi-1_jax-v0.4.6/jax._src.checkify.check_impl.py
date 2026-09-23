@check_p.def_impl
def check_impl(*args, err_tree, debug):
  if debug:
    # NOOP (check will only trigger when discharged)
    return []
  error = tree_unflatten(err_tree, args)
  exc = error.get_exception()
  if exc:
    raise JaxRuntimeError(str(exc)) from exc
  return []
