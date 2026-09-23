  @classmethod
  def from_mrp(cls, mrp: jax.Array):
    """Initialize from Modified Rodrigues Parameters (MRPs)."""
    return cls(_from_mrp(mrp))
