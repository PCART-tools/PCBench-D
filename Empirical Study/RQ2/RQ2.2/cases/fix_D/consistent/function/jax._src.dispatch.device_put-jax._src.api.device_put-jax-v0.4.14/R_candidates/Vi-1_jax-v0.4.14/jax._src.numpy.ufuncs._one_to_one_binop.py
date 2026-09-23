def _one_to_one_binop(
    numpy_fn: Callable[..., Any], lax_fn: BinOp,
    promote_to_inexact: bool = False, lax_doc: bool = False,
    promote_to_numeric: bool = False) -> BinOp:
  if promote_to_inexact:
    fn = lambda x1, x2, /: lax_fn(*promote_args_inexact(numpy_fn.__name__, x1, x2))
  elif promote_to_numeric:
    fn = lambda x1, x2, /: lax_fn(*promote_args_numeric(numpy_fn.__name__, x1, x2))
  else:
    fn = lambda x1, x2, /: lax_fn(*promote_args(numpy_fn.__name__, x1, x2))
  fn.__qualname__ = f"jax.numpy.{numpy_fn.__name__}"
  fn = jit(fn, inline=True)
  if lax_doc:
    doc = dedent('\n\n'.join(lax_fn.__doc__.split('\n\n')[1:])).strip()  # type: ignore[union-attr]
    return _wraps(numpy_fn, lax_description=doc, module='numpy')(fn)
  else:
    return _wraps(numpy_fn, module='numpy')(fn)
