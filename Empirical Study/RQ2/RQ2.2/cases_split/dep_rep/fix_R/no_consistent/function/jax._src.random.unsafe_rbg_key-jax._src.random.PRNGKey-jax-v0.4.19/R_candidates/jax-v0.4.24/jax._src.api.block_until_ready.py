def block_until_ready(x):
  """
  Tries to call a ``block_until_ready`` method on pytree leaves.

  Args:
    x: a pytree, usually with at least some JAX array instances at its leaves.

  Returns:
    A pytree with the same structure and values of the input, where the values
    of all JAX array leaves are ready.
  """
  def try_to_block(x):
    try:
      return x.block_until_ready()
    except AttributeError:
      return x
  return tree_map(try_to_block, x)
