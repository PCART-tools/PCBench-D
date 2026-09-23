def _comparison_op(numpy_fn: Callable[..., Any], lax_fn: BinOp) -> BinOp:
  def fn(x1, x2, /):
    x1, x2 =  _promote_args(numpy_fn.__name__, x1, x2)
    # Comparison on complex types are defined as a lexicographic ordering on
    # the (real, imag) pair.
    if dtypes.issubdtype(dtypes.dtype(x1), np.complexfloating):
      rx = lax.real(x1)
      ry = lax.real(x2)
      return lax.select(lax.eq(rx, ry), lax_fn(lax.imag(x1), lax.imag(x2)),
                        lax_fn(rx, ry))
    return lax_fn(x1, x2)
  fn.__qualname__ = f"jax.numpy.{numpy_fn.__name__}"
  fn = jit(fn, inline=True)
  return _wraps(numpy_fn, module='numpy')(fn)
