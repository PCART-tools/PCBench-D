  @classmethod
  def from_quat(cls, quat: jax.Array):
    """Initialize from quaternions."""
    return cls(_normalize_quaternion(quat))
