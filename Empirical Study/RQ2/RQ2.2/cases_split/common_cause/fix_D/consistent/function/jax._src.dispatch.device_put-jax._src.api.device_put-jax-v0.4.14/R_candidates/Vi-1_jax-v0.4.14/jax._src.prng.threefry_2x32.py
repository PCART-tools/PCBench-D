@partial(jit, inline=True)
def threefry_2x32(keypair, count):
  """Apply the Threefry 2x32 hash.

  Args:
    keypair: a pair of 32bit unsigned integers used for the key.
    count: an array of dtype uint32 used for the counts.

  Returns:
    An array of dtype uint32 with the same shape as `count`.
  """
  key1, key2 = keypair
  if not lax.dtype(key1) == lax.dtype(key2) == lax.dtype(count) == np.uint32:
    msg = "threefry_2x32 requires uint32 arguments, got {}"
    raise TypeError(msg.format([lax.dtype(x) for x in [key1, key2, count]]))

  odd_size = count.size % 2
  if not isinstance(odd_size, int):
    msg = ("jax.random functions have limited support for shape polymorphism. "
           "In particular, the product of the known dimensions must be even.")
    raise core.InconclusiveDimensionOperation(msg)

  if odd_size:
    x = list(jnp.split(jnp.concatenate([count.ravel(), np.uint32([0])]), 2))
  else:
    x = list(jnp.split(count.ravel(), 2))

  x = threefry2x32_p.bind(key1, key2, x[0], x[1])
  out = jnp.concatenate(x)
  assert out.dtype == np.uint32
  return lax.reshape(out[:-1] if odd_size else out, count.shape)
