  def mean(self, weights: jax.Array | None = None):
    """Get the mean of the rotations."""
    w = jnp.ones(self.quat.shape[0], dtype=self.quat.dtype) if weights is None else jnp.asarray(weights, dtype=self.quat.dtype)
    if w.ndim != 1:
      raise ValueError("Expected `weights` to be 1 dimensional, got "
                       "shape {}.".format(w.shape))
    if w.shape[0] != len(self):
      raise ValueError("Expected `weights` to have number of values "
                       "equal to number of rotations, got "
                       "{} values and {} rotations.".format(w.shape[0], len(self)))
    K = jnp.dot(w[jnp.newaxis, :] * self.quat.T, self.quat)
    _, v = jnp.linalg.eigh(K)
    return Rotation(v[:, -1])
