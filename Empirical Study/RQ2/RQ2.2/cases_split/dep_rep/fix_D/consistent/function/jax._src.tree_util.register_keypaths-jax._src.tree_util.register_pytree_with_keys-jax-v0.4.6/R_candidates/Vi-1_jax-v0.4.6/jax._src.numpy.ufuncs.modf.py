@_wraps(np.modf, module='numpy', skip_params=['out'])
@jit
def modf(x: ArrayLike, /, out=None) -> Tuple[Array, Array]:
  _check_arraylike("modf", x)
  x, = _promote_dtypes_inexact(x)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.modf is not supported.")
  whole = _where(lax.ge(x, lax._zero(x)), floor(x), ceil(x))
  return x - whole, whole
