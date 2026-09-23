def _check(pred, msg, debug, *fmt_args, **fmt_kwargs):
  if not is_scalar_pred(pred):
    prim_name = 'debug_check' if debug else 'check'
    raise TypeError(f'{prim_name} takes a scalar pred as argument, got {pred}')
  for arg in jtu.tree_leaves((fmt_args, fmt_kwargs)):
    if not isinstance(arg, (jax.Array, np.ndarray)):
      raise TypeError('Formatting arguments to checkify.check need to be '
                      'PyTrees of arrays, but got '
                      f'{repr(arg)} of type {type(arg)}.')
  new_error = FailedCheckError(summary(), msg, *fmt_args, **fmt_kwargs)
  error = assert_func(init_error, jnp.logical_not(pred), new_error)
  _check_error(error, debug=debug)
