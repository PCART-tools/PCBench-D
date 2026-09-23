def _block(xs: Union[ArrayLike, list[ArrayLike]]) -> tuple[Array, int]:
  if isinstance(xs, tuple):
    raise ValueError("jax.numpy.block does not allow tuples, got {}"
                     .format(xs))
  elif isinstance(xs, list):
    if len(xs) == 0:
      raise ValueError("jax.numpy.block does not allow empty list arguments")
    xs_tup, depths = unzip2([_block(x) for x in xs])
    if any(d != depths[0] for d in depths[1:]):
      raise ValueError("Mismatched list depths in jax.numpy.block")
    rank = max(depths[0], max(ndim(x) for x in xs_tup))
    xs_tup = tuple(_atleast_nd(x, rank) for x in xs_tup)
    return concatenate(xs_tup, axis=-depths[0]), depths[0] + 1
  else:
    return asarray(xs), 1
