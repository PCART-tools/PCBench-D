  def as_matrix(self) -> jax.Array:
    """Represent as rotation matrix."""
    return _as_matrix(self.quat)
