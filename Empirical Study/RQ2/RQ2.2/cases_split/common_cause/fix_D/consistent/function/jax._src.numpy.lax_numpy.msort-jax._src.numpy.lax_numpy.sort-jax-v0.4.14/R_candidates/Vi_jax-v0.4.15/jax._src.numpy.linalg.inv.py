@_wraps(np.linalg.inv)
@jit
def inv(a: ArrayLike) -> Array:
  check_arraylike("jnp.linalg.inv", a)
  arr = jnp.asarray(a)
  if arr.ndim < 2 or arr.shape[-1] != arr.shape[-2]:
    raise ValueError(
      f"Argument to inv must have shape [..., n, n], got {arr.shape}.")
  return solve(
    arr, lax.broadcast(jnp.eye(arr.shape[-1], dtype=arr.dtype), arr.shape[:-2]))
