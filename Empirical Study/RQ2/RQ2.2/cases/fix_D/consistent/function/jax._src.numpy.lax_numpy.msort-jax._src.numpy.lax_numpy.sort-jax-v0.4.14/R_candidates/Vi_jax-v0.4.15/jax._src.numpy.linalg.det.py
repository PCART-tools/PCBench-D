@custom_jvp
@_wraps(np.linalg.det)
@jit
def det(a: ArrayLike) -> Array:
  check_arraylike("jnp.linalg.det", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  a_shape = jnp.shape(a)
  if len(a_shape) >= 2 and a_shape[-1] == 2 and a_shape[-2] == 2:
    return _det_2x2(a)
  elif len(a_shape) >= 2 and a_shape[-1] == 3 and a_shape[-2] == 3:
    return _det_3x3(a)
  elif len(a_shape) >= 2 and a_shape[-1] == a_shape[-2]:
    sign, logdet = slogdet(a)
    return sign * ufuncs.exp(logdet).astype(sign.dtype)
  else:
    msg = "Argument to _det() must have shape [..., n, n], got {}"
    raise ValueError(msg.format(a_shape))
