  def __init__(self, dataset, bw_method=None, weights=None):
    check_arraylike("gaussian_kde", dataset)
    dataset = jnp.atleast_2d(dataset)
    if jnp.issubdtype(lax.dtype(dataset), jnp.complexfloating):
      raise NotImplementedError("gaussian_kde does not support complex data")
    if not dataset.size > 1:
      raise ValueError("`dataset` input should have multiple elements.")

    d, n = dataset.shape
    if weights is not None:
      check_arraylike("gaussian_kde", weights)
      dataset, weights = promote_dtypes_inexact(dataset, weights)
      weights = jnp.atleast_1d(weights)
      weights /= jnp.sum(weights)
      if weights.ndim != 1:
        raise ValueError("`weights` input should be one-dimensional.")
      if len(weights) != n:
        raise ValueError("`weights` input should be of length n")
    else:
      dataset, = promote_dtypes_inexact(dataset)
      weights = jnp.full(n, 1.0 / n, dtype=dataset.dtype)

    self._setattr("dataset", dataset)
    self._setattr("weights", weights)
    neff = self._setattr("neff", 1 / jnp.sum(weights**2))

    bw_method = "scott" if bw_method is None else bw_method
    if bw_method == "scott":
      factor = jnp.power(neff, -1. / (d + 4))
    elif bw_method == "silverman":
      factor = jnp.power(neff * (d + 2) / 4.0, -1. / (d + 4))
    elif jnp.isscalar(bw_method) and not isinstance(bw_method, str):
      factor = bw_method
    elif callable(bw_method):
      factor = bw_method(self)
    else:
      raise ValueError(
          "`bw_method` should be 'scott', 'silverman', a scalar, or a callable."
      )

    data_covariance = jnp.atleast_2d(
        jnp.cov(dataset, rowvar=1, bias=False, aweights=weights))
    data_inv_cov = jnp.linalg.inv(data_covariance)
    covariance = data_covariance * factor**2
    inv_cov = data_inv_cov / factor**2
    self._setattr("covariance", covariance)
    self._setattr("inv_cov", inv_cov)
