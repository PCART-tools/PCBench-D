@_wraps(osp_stats.multivariate_normal.logpdf, update_doc=False, lax_description="""
In the JAX version, the `allow_singular` argument is not implemented.
""")
def logpdf(x, mean, cov, allow_singular=None):
  if allow_singular is not None:
    raise NotImplementedError("allow_singular argument of multivariate_normal.logpdf")
  x, mean, cov = _promote_dtypes_inexact(x, mean, cov)
  if not mean.shape:
    return (-1/2 * jnp.square(x - mean) / cov
            - 1/2 * (jnp.log(2*np.pi) + jnp.log(cov)))
  else:
    n = mean.shape[-1]
    if not np.shape(cov):
      y = x - mean
      return (-1/2 * jnp.einsum('...i,...i->...', y, y) / cov
              - n/2 * (jnp.log(2*np.pi) + jnp.log(cov)))
    else:
      if cov.ndim < 2 or cov.shape[-2:] != (n, n):
        raise ValueError("multivariate_normal.logpdf got incompatible shapes")
      L = lax.linalg.cholesky(cov)
      y = jnp.vectorize(
        partial(lax.linalg.triangular_solve, lower=True, transpose_a=True),
        signature="(n,n),(n)->(n)"
      )(L, x - mean)
      return (-1/2 * jnp.einsum('...i,...i->...', y, y) - n/2 * jnp.log(2*np.pi)
              - jnp.log(L.diagonal(axis1=-1, axis2=-2)).sum(-1))
