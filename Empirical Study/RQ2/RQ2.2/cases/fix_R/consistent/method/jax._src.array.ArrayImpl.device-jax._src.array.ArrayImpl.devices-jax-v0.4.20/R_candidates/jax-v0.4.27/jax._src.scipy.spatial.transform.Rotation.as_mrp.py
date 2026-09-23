  def as_mrp(self) -> jax.Array:
    """Represent as Modified Rodrigues Parameters (MRPs)."""
    return _as_mrp(self.quat)
