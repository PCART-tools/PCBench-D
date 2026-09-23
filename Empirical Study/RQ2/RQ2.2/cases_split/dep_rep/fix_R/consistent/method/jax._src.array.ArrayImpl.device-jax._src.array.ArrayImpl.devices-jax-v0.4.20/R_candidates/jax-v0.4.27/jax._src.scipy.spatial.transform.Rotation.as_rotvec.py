  def as_rotvec(self, degrees: bool = False) -> jax.Array:
    """Represent as rotation vectors."""
    return _as_rotvec(self.quat, degrees)
