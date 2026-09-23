@implements(np.isfinite, module='numpy')
@partial(jit, inline=True)
def isfinite(x: ArrayLike, /) -> Array:
  check_arraylike("isfinite", x)
  dtype = dtypes.dtype(x)
  if dtypes.issubdtype(dtype, np.floating):
    return lax.is_finite(x)
  elif dtypes.issubdtype(dtype, np.complexfloating):
    return lax.bitwise_and(lax.is_finite(real(x)), lax.is_finite(imag(x)))
  else:
    return lax.full_like(x, True, dtype=np.bool_)
