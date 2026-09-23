@util._wraps(np.fromfunction)
def fromfunction(function: Callable[..., Array], shape: Any,
                 *, dtype: DTypeLike = float, **kwargs) -> Array:
  shape = core.canonicalize_shape(shape, context="shape argument of jnp.fromfunction()")
  for i in range(len(shape)):
    in_axes = [0 if i == j else None for j in range(len(shape))]
    function = jax.vmap(function, in_axes=tuple(in_axes[::-1]))
  return function(*(arange(s, dtype=dtype) for s in shape), **kwargs)
