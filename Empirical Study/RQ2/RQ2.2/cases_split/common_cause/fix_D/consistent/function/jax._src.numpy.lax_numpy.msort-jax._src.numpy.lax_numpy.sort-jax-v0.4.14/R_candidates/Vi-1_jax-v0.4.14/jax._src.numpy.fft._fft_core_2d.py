def _fft_core_2d(func_name: str, fft_type: xla_client.FftType, a: ArrayLike,
                 s: Optional[Shape], axes: Sequence[int],
                 norm: Optional[str]) -> Array:
  full_name = "jax.numpy.fft." + func_name
  if len(axes) != 2:
    raise ValueError(
        "%s only supports 2 axes. Got axes = %r."
        % (full_name, axes)
    )
  return _fft_core(func_name, fft_type, a, s, axes, norm)
