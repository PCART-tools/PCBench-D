@_wraps(osp_fft.dct)
def dct(x: Array, type: int = 2, n: Optional[int] = None,
        axis: int = -1, norm: Optional[str] = None) -> Array:
  if type != 2:
    raise NotImplementedError('Only DCT type 2 is implemented.')

  axis = canonicalize_axis(axis, x.ndim)
  if n is not None:
    x = lax.pad(x, jnp.array(0, x.dtype),
                [(0, n - x.shape[axis] if a == axis else 0, 0)
                 for a in range(x.ndim)])

  N = x.shape[axis]
  v = _dct_interleave(x, axis)
  V = jnp.fft.fft(v, axis=axis)
  k = lax.expand_dims(jnp.arange(N, dtype=V.real.dtype), [a for a in range(x.ndim) if a != axis])
  out = V * _W4(N, k)
  out = 2 * out.real
  if norm == 'ortho':
    out = _dct_ortho_norm(out, axis)
  return out
