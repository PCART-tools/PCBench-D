  @staticmethod
  def create(capacity: int, prototype: Any) -> Stack:
    """Creates a stack with size `capacity` with elements like `prototype`.

    `prototype` can be any JAX pytree. This function looks only at its
    structure; the specific values are ignored.
    """
    return Stack(
      jnp.array(0, jnp.int32),
      jax.tree_util.tree_map(
        lambda x: jnp.zeros((capacity,) + tuple(x.shape), x.dtype), prototype))
