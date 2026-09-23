@_wraps(osp_fft.idctn)
def idctn(x: Array, type: int = 2,
         s: Optional[Sequence[int]]=None,
         axes: Optional[Sequence[int]] = None,
         norm: Optional[str] = None) -> Array:
  if type != 2:
    raise NotImplementedError('Only DCT type 2 is implemented.')

  if axes is None:
    axes = range(x.ndim)

  if len(axes) == 1:
    return idct(x, n=s[0] if s is not None else None, axis=axes[0], norm=norm)

  if s is not None:
    ns = {a: n for a, n in zip(axes, s)}
    pads = [(0, ns[a] - x.shape[a] if a in ns else 0, 0) for a in range(x.ndim)]
    x = lax.pad(x, jnp.array(0, x.dtype), pads)

  # compose high-D DCTs from 1D DCTs:
  for axis in axes:
    x = idct(x, axis=axis, norm=norm)
  return x
