  def integrate_box_1d(self, low, high):
    """Integrate the distribution over the given limits."""
    if self.d != 1:
      raise ValueError("integrate_box_1d() only handles 1D pdfs")
    if jnp.ndim(low) != 0 or jnp.ndim(high) != 0:
      raise ValueError(
          "the limits of integration in integrate_box_1d must be scalars")
    sigma = jnp.squeeze(jnp.sqrt(self.covariance))
    low = jnp.squeeze((low - self.dataset) / sigma)
    high = jnp.squeeze((high - self.dataset) / sigma)
    return jnp.sum(self.weights * (special.ndtr(high) - special.ndtr(low)))
