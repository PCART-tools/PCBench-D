@partial(jit, static_argnums=(1, 2), inline=True)
def _threefry_random_bits_original(key: jax.Array, bit_width, shape):
  size = math.prod(shape)
  # Compute ceil(bit_width * size / 32) in a way that is friendly to shape
  # polymorphism
  max_count, r = divmod(bit_width * size, 32)
  if r > 0:
    max_count += 1

  if core.is_constant_dim(max_count):
    nblocks, rem = divmod(max_count, jnp.iinfo(np.uint32).max)
  else:
    nblocks, rem = 0, max_count

  if not nblocks:
    bits = threefry_2x32(key, lax.iota(np.uint32, rem))
  else:
    keys = threefry_split(key, nblocks + 1)
    subkeys, last_key = keys[:-1], keys[-1]
    blocks = vmap(threefry_2x32, in_axes=(0, None))(subkeys, lax.iota(np.uint32, jnp.iinfo(np.uint32).max))
    last = threefry_2x32(last_key, lax.iota(np.uint32, rem))
    bits = lax.concatenate([blocks.ravel(), last], 0)

  dtype = UINT_DTYPES[bit_width]
  if bit_width == 64:
    bits = [lax.convert_element_type(x, dtype) for x in jnp.split(bits, 2)]
    bits = lax.shift_left(bits[0], dtype(32)) | bits[1]
  elif bit_width in [8, 16]:
    # this is essentially bits.view(dtype)[:size]
    bits = lax.bitwise_and(
      np.uint32(np.iinfo(dtype).max),
      lax.shift_right_logical(
        lax.broadcast(bits, (1,)),
        lax.mul(
          np.uint32(bit_width),
          lax.broadcasted_iota(np.uint32, (32 // bit_width, 1), 0)
        )
      )
    )
    bits = lax.reshape(bits, ((max_count * 32 // bit_width),), (1, 0))
    bits = lax.convert_element_type(bits, dtype)[:size]
  return lax.reshape(bits, shape)
