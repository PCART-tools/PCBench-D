@_wraps(np.polyval, lax_description="""\
The ``unroll`` parameter is JAX specific. It does not effect correctness but can
have a major impact on performance for evaluating high-order polynomials. The
parameter controls the number of unrolled steps with ``lax.scan`` inside the
``polyval`` implementation. Consider setting ``unroll=128`` (or even higher) to
improve runtime performance on accelerators, at the cost of increased
compilation time.
""")
@partial(jit, static_argnames=['unroll'])
def polyval(p: Array, x: Array, *, unroll: int = 16) -> Array:
  check_arraylike("polyval", p, x)
  p, x = promote_dtypes_inexact(p, x)
  shape = lax.broadcast_shapes(p.shape[1:], x.shape)
  y = lax.full_like(x, 0, shape=shape, dtype=x.dtype)
  y, _ = lax.scan(lambda y, p: (y * x + p, None), y, p, unroll=unroll)
  return y
