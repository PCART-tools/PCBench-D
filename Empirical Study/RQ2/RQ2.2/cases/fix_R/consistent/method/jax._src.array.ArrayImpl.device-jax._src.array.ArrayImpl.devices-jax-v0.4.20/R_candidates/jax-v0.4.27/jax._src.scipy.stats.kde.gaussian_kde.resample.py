  def resample(self, key, shape=()):
    r"""Randomly sample a dataset from the estimated pdf

    Args:
      key: a PRNG key used as the random key.
      shape: optional, a tuple of nonnegative integers specifying the result
        batch shape; that is, the prefix of the result shape excluding the last
        axis.

    Returns:
      The resampled dataset as an array with shape `(d,) + shape`.
    """
    ind_key, eps_key = random.split(key)
    ind = random.choice(ind_key, self.n, shape=shape, p=self.weights)
    eps = random.multivariate_normal(eps_key,
                                     jnp.zeros(self.d, self.covariance.dtype),
                                     self.covariance,
                                     shape=shape,
                                     dtype=self.dataset.dtype).T
    return self.dataset[:, ind] + eps
