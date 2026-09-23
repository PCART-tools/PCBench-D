  def apply(self, vectors: jax.Array, inverse: bool = False) -> jax.Array:
    """Apply this rotation to one or more vectors."""
    return _apply(self.as_matrix(), vectors, inverse)
