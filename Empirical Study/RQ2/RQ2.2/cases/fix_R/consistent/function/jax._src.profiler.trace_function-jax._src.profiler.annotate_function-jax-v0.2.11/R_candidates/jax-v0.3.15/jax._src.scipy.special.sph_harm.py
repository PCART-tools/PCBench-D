def sph_harm(m: jnp.ndarray,
             n: jnp.ndarray,
             theta: jnp.ndarray,
             phi: jnp.ndarray,
             n_max: Optional[int] = None) -> jnp.ndarray:
  r"""Computes the spherical harmonics.

  The JAX version has one extra argument `n_max`, the maximum value in `n`.

  The spherical harmonic of degree `n` and order `m` can be written as
  :math:`Y_n^m(\theta, \phi) = N_n^m * P_n^m(\cos \phi) * \exp(i m \theta)`,
  where :math:`N_n^m = \sqrt{\frac{\left(2n+1\right) \left(n-m\right)!}
  {4 \pi \left(n+m\right)!}}` is the normalization factor and :math:`\phi` and
  :math:\theta` are the colatitude and longitude, repectively. :math:`N_n^m` is
  chosen in the way that the spherical harmonics form a set of orthonormal basis
  functions of :math:`L^2(S^2)`.

  Args:
    m: The order of the harmonic; must have `|m| <= n`. Return values for
      `|m| > n` ara undefined.
    n: The degree of the harmonic; must have `n >= 0`. The standard notation for
      degree in descriptions of spherical harmonics is `l (lower case L)`. We
      use `n` here to be consistent with `scipy.special.sph_harm`. Return
      values for `n < 0` are undefined.
    theta: The azimuthal (longitudinal) coordinate; must be in [0, 2*pi].
    phi: The polar (colatitudinal) coordinate; must be in [0, pi].
    n_max: The maximum degree `max(n)`. If the supplied `n_max` is not the true
      maximum value of `n`, the results are clipped to `n_max`. For example,
      `sph_harm(m=jnp.array([2]), n=jnp.array([10]), theta, phi, n_max=6)`
      acutually returns
      `sph_harm(m=jnp.array([2]), n=jnp.array([6]), theta, phi, n_max=6)`
  Returns:
    A 1D array containing the spherical harmonics at (m, n, theta, phi).
  """

  if jnp.isscalar(phi):
    phi = jnp.array([phi])

  if n_max is None:
    n_max = jnp.max(n)
  n_max = core.concrete_or_error(
      int, n_max, 'The `n_max` argument of `jnp.scipy.special.sph_harm` must '
      'be statically specified to use `sph_harm` within JAX transformations.')

  return _sph_harm(m, n, theta, phi, n_max)
