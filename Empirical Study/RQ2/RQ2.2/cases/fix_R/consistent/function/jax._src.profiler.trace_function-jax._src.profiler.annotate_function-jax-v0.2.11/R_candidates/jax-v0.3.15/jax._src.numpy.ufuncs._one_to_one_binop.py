def _one_to_one_binop(numpy_fn, lax_fn, promote_to_inexact=False, lax_doc=False):
  if promote_to_inexact:
    fn = lambda x1, x2: lax_fn(*_promote_args_inexact(numpy_fn.__name__, x1, x2))
  else:
    fn = lambda x1, x2: lax_fn(*_promote_args(numpy_fn.__name__, x1, x2))
  fn = jit(fn, inline=True)
  if lax_doc:
    doc = dedent('\n\n'.join(lax_fn.__doc__.split('\n\n')[1:])).strip()
    return _wraps(numpy_fn, lax_description=doc, module='numpy')(fn)
  else:
    return _wraps(numpy_fn, module='numpy')(fn)
