@implements(osp_fft.dct)
def idct(x: Array, type: int = 2, n: int | None = None,
        axis: int = -1, norm: str | None = None) -> Array:
  if type != 2:
    raise NotImplementedError('Only DCT type 2 is implemented.')

  axis = canonicalize_axis(axis, x.ndim)
  if n is not None:
    x = lax.pad(x, jnp.array(0, x.dtype),
                [(0, n - x.shape[axis] if a == axis else 0, 0)
                 for a in range(x.ndim)])
  N = x.shape[axis]
  x = x.astype(jnp.float32)
  if norm is None:
    x = _dct_ortho_norm(x, axis)
  x = _dct_ortho_norm(x, axis)


  k = lax.expand_dims(jnp.arange(N, dtype=jnp.float32), [a for a in range(x.ndim) if a != axis])
  # everything is complex from here...
  w4 = _W4(N,k)
  x = x.astype(w4.dtype)
  x = x / (_W4(N, k))
  x = x * 2 * N

  x = jnp.fft.ifft(x, axis=axis)
  # convert back to reals..
  out = _dct_deinterleave(x.real, axis)
  return out
