@_wraps(osp_signal.fftconvolve)
def fftconvolve(in1: ArrayLike, in2: ArrayLike, mode: str = "full",
                axes: Optional[Sequence[int]] = None) -> Array:
  check_arraylike('fftconvolve', in1, in2)
  in1, in2 = promote_dtypes_inexact(in1, in2)
  if in1.ndim != in2.ndim:
    raise ValueError("in1 and in2 should have the same dimensionality")
  if mode not in ["same", "full", "valid"]:
    raise ValueError("mode must be one of ['same', 'full', 'valid']")
  _fftconvolve = partial(_fftconvolve_unbatched, mode=mode)
  if axes is None:
    return _fftconvolve(in1, in2)
  axes = _ensure_index_tuple(axes)
  axes = tuple(canonicalize_axis(ax, in1.ndim) for ax in axes)
  mapped_axes = set(range(in1.ndim)) - set(axes)
  if any(in1.shape[i] != in2.shape[i] for i in mapped_axes):
    raise ValueError(f"mapped axes must have same shape; got {in1.shape=} {in2.shape=} {axes=}")
  for ax in sorted(mapped_axes):
    _fftconvolve = jax.vmap(_fftconvolve, in_axes=ax, out_axes=ax)
  return _fftconvolve(in1, in2)
