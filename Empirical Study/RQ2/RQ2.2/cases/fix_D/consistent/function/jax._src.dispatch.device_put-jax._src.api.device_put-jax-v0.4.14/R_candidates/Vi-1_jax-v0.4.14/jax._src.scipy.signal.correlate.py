@_wraps(osp_signal.correlate)
def correlate(in1: Array, in2: Array, mode: str = 'full', method: str = 'auto',
              precision: PrecisionLike = None) -> Array:
  return convolve(in1, jnp.flip(in2.conj()), mode, precision=precision, method=method)
