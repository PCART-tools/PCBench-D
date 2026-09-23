def _not_implemented(fun, module=None):
  @_wraps(fun, module=module, update_doc=False, lax_description=_NOT_IMPLEMENTED_DESC)
  def wrapped(*args, **kwargs):
    msg = "Numpy function {} not yet implemented"
    raise NotImplementedError(msg.format(fun))
  return wrapped
