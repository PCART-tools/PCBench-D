@implements(np.fft.ifftshift)
def ifftshift(x: ArrayLike, axes: None | int | Sequence[int] = None) -> Array:
  check_arraylike("ifftshift", x)
  x = jnp.asarray(x)
  shift: int | Sequence[int]
  if axes is None:
    axes = tuple(range(x.ndim))
    shift = [-(dim // 2) for dim in x.shape]
  elif isinstance(axes, int):
    shift = -(x.shape[axes] // 2)
  else:
    shift = [-(x.shape[ax] // 2) for ax in axes]

  return jnp.roll(x, shift, axes)
