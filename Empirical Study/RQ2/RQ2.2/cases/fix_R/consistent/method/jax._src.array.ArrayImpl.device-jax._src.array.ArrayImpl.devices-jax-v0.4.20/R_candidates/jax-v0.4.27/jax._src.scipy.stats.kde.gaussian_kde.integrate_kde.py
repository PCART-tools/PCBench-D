  def integrate_kde(self, other):
    """Integrate the product of two Gaussian KDE distributions."""
    if other.d != self.d:
      raise ValueError("KDEs are not the same dimensionality")

    chol = linalg.cho_factor(self.covariance + other.covariance)
    norm = jnp.sqrt(2 * np.pi)**self.d * jnp.prod(jnp.diag(chol[0]))
    norm = 1.0 / norm

    sm, lg = (self, other) if self.n < other.n else (other, self)
    result = vmap(partial(_gaussian_kernel_convolve, chol, norm, lg.dataset,
                          lg.weights),
                  in_axes=1)(sm.dataset)
    return jnp.sum(result * sm.weights)
