@implements(osp_signal.convolve2d)
def convolve2d(in1: Array, in2: Array, mode: str = 'full', boundary: str = 'fill',
               fillvalue: float = 0, precision: PrecisionLike = None) -> Array:
  if boundary != 'fill' or fillvalue != 0:
    raise NotImplementedError("convolve2d() only supports boundary='fill', fillvalue=0")
  if jnp.ndim(in1) != 2 or jnp.ndim(in2) != 2:
    raise ValueError("convolve2d() only supports 2-dimensional inputs.")
  return _convolve_nd(in1, in2, mode, precision=precision)
