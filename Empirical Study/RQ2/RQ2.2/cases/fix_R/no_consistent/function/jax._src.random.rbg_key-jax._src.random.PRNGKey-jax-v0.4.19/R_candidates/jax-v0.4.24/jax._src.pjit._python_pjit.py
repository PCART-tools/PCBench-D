def _python_pjit(fun: Callable, infer_params_fn):

  @wraps(fun)
  @api_boundary
  def wrapped(*args, **kwargs):
    if config.disable_jit.value:
      return fun(*args, **kwargs)
    return _python_pjit_helper(fun, infer_params_fn, *args, **kwargs)[0]

  def _python_pjit_evict_fn():
    _create_pjit_jaxpr.evict_function(fun)  # type: ignore
  wrapped.clear_cache = _python_pjit_evict_fn
  return wrapped
