  def magnitude(self) -> jax.Array:
    """Get the magnitude(s) of the rotation(s)."""
    return _magnitude(self.quat)
