@custom_jvp
@_wraps(np.logaddexp2, module='numpy')
@jit
def logaddexp2(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  x1, x2 = _promote_args_inexact("logaddexp2", x1, x2)
  amax = lax.max(x1, x2)
  if dtypes.issubdtype(x1.dtype, np.floating):
    delta = lax.sub(x1, x2)
    return lax.select(lax._isnan(delta),
                      lax.add(x1, x2),  # NaNs or infinities of the same sign.
                      lax.add(amax, lax.div(lax.log1p(exp2(lax.neg(lax.abs(delta)))),
                                            _constant_like(x1, np.log(2)))))
  else:
    delta = lax.sub(lax.add(x1, x2), lax.mul(amax, _constant_like(amax, 2)))
    out = lax.add(amax, lax.div(lax.log1p(exp2(delta)), _constant_like(x1, np.log(2))))
    return lax.complex(lax.real(out), _wrap_between(lax.imag(out), np.pi / np.log(2)))
