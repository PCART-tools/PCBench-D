@implements(getattr(np.linalg, "matrix_transpose", None))
def matrix_transpose(x: ArrayLike, /) -> Array:
  """Transposes a matrix (or a stack of matrices) x."""
  check_arraylike('jnp.linalg.matrix_transpose', x)
  x_arr = jnp.asarray(x)
  ndim = x_arr.ndim
  if ndim < 2:
    raise ValueError(f"matrix_transpose requres at least 2 dimensions; got {ndim=}")
  return jax.lax.transpose(x_arr, (*range(ndim - 2), ndim - 1, ndim - 2))
