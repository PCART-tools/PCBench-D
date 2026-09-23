def _maybe_bool_binop(numpy_fn, lax_fn, bool_lax_fn, lax_doc=False):
  def fn(x1, x2):
    x1, x2 = _promote_args(numpy_fn.__name__, x1, x2)
    return lax_fn(x1, x2) if x1.dtype != np.bool_ else bool_lax_fn(x1, x2)
  fn = jit(fn, inline=True)
  if lax_doc:
    doc = dedent('\n\n'.join(lax_fn.__doc__.split('\n\n')[1:])).strip()
    return _wraps(numpy_fn, lax_description=doc, module='numpy')(fn)
  else:
    return _wraps(numpy_fn, module='numpy')(fn)
