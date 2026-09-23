@_wraps(osp_signal.correlate2d)
def correlate2d(in1, in2, mode='full', boundary='fill', fillvalue=0,
                precision=None):
  if boundary != 'fill' or fillvalue != 0:
    raise NotImplementedError("correlate2d() only supports boundary='fill', fillvalue=0")
  if jnp.ndim(in1) != 2 or jnp.ndim(in2) != 2:
    raise ValueError("correlate2d() only supports 2-dimensional inputs.")

  swap = all(s1 <= s2 for s1, s2 in zip(in1.shape, in2.shape))
  same_shape =  all(s1 == s2 for s1, s2 in zip(in1.shape, in2.shape))

  if mode == "same":
    in1, in2 = jnp.flip(in1), in2.conj()
    result = jnp.flip(_convolve_nd(in1, in2, mode, precision=precision))
  elif mode == "valid":
    if swap and not same_shape:
      in1, in2 = jnp.flip(in2), in1.conj()
      result = _convolve_nd(in1, in2, mode, precision=precision)
    else:
      in1, in2 = jnp.flip(in1), in2.conj()
      result = jnp.flip(_convolve_nd(in1, in2, mode, precision=precision))
  else:
    if swap:
      in1, in2 = jnp.flip(in2), in1.conj()
      result = _convolve_nd(in1, in2, mode, precision=precision).conj()
    else:
      in1, in2 = jnp.flip(in1), in2.conj()
      result = jnp.flip(_convolve_nd(in1, in2, mode, precision=precision))
  return result
