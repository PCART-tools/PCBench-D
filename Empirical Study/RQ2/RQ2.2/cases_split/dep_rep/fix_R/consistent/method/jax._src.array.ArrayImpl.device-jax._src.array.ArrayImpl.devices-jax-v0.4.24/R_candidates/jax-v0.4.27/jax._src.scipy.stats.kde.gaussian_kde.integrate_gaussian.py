  def integrate_gaussian(self, mean, cov):
    """Integrate the distribution weighted by a Gaussian."""
    mean = jnp.atleast_1d(jnp.squeeze(mean))
    cov = jnp.atleast_2d(cov)

    if mean.shape != (self.d,):
      raise ValueError(f"mean does not have dimension {self.d}")
    if cov.shape != (self.d, self.d):
      raise ValueError(f"covariance does not have dimension {self.d}")

    chol = linalg.cho_factor(self.covariance + cov)
    norm = jnp.sqrt(2 * np.pi)**self.d * jnp.prod(jnp.diag(chol[0]))
    norm = 1.0 / norm
    return _gaussian_kernel_convolve(chol, norm, self.dataset, self.weights,
                                     mean)
