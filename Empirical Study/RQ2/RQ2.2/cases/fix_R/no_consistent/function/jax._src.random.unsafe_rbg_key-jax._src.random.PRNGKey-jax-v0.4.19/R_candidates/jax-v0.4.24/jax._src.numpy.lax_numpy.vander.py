@util.implements(np.vander)
@partial(jit, static_argnames=('N', 'increasing'))
def vander(
    x: ArrayLike, N: int | None = None, increasing: bool = False
) -> Array:
  util.check_arraylike("vander", x)
  x = asarray(x)
  if x.ndim != 1:
    raise ValueError("x must be a one-dimensional array")
  N = x.shape[0] if N is None else core.concrete_or_error(
    operator.index, N, "'N' argument of jnp.vander()")
  if N < 0:
    raise ValueError("N must be nonnegative")

  iota = lax.iota(x.dtype, N)
  if not increasing:
    iota = lax.sub(_lax_const(iota, N - 1), iota)

  return ufuncs.power(x[..., None], expand_dims(iota, tuple(range(x.ndim))))
