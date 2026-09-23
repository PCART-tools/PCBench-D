def polar_unitary(a, *, method="qdwh", eps=None, max_iterations=None):
  """ Computes the unitary factor u in the polar decomposition ``a = u p``
  (or ``a = p u``).

  .. warning::
    This function is deprecated. Use :func:`jax.scipy.linalg.polar` instead.
  """
  # TODO(phawkins): delete this function after 2022/8/11.
  warnings.warn("jax.scipy.linalg.polar_unitary is deprecated. Call "
                "jax.scipy.linalg.polar instead.",
                DeprecationWarning)
  unitary, _ = polar(a, method, eps, max_iterations)
  return unitary
