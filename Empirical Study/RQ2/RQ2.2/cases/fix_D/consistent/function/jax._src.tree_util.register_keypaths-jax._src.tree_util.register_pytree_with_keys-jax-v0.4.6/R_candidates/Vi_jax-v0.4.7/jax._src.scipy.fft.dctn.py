@_wraps(osp_fft.dctn)
def dctn(x: Array, type: int = 2,
         s: Optional[Sequence[int]]=None,
         axes: Optional[Sequence[int]] = None,
         norm: Optional[str] = None) -> Array:
  if type != 2:
    raise NotImplementedError('Only DCT type 2 is implemented.')

  if axes is None:
    axes = range(x.ndim)

  if len(axes) == 1:
    return dct(x, n=s[0] if s is not None else None, axis=axes[0], norm=norm)

  if s is not None:
    ns = {a: n for a, n in zip(axes, s)}
    pads = [(0, ns[a] - x.shape[a] if a in ns else 0, 0) for a in range(x.ndim)]
    x = lax.pad(x, jnp.array(0, x.dtype), pads)

  if len(axes) == 2:
    return _dct2(x, axes=axes, norm=norm)

  # compose high-D DCTs from 2D and 1D DCTs:
  for axes_block in [axes[i:i+2] for i in range(0, len(axes), 2)]:
    x = dctn(x, axes=axes_block, norm=norm)
  return x
