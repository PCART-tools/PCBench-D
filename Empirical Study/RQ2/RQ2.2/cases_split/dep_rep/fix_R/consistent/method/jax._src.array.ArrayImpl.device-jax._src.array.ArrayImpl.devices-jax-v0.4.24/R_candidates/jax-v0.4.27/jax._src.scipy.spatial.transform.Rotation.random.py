  @classmethod
  def random(cls, random_key: jax.Array, num: int | None = None):
    """Generate uniformly distributed rotations."""
    # Need to implement scipy.stats.special_ortho_group for this to work...
    raise NotImplementedError()
