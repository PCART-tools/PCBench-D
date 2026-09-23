def _comparison_op(numpy_fn, lax_fn):
  # TODO(https://github.com/google/jax/issues/6713): decorate this function with
  # jit, after fixing a surprising interaction with remat(..., concrete=True).
  def fn(x1, x2):
    x1, x2 =  _promote_args(numpy_fn.__name__, x1, x2)
    # Comparison on complex types are defined as a lexicographic ordering on
    # the (real, imag) pair.
    if dtypes.issubdtype(dtypes.dtype(x1), np.complexfloating):
      rx = lax.real(x1)
      ry = lax.real(x2)
      return lax.select(lax.eq(rx, ry), lax_fn(lax.imag(x1), lax.imag(x2)),
                        lax_fn(rx, ry))
    return lax_fn(x1, x2)
  return _wraps(numpy_fn, module='numpy')(fn)
