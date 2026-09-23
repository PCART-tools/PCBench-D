@util._wraps(np.put, lax_description="""
Numpy function :func:`numpy.put` is not available in JAX and will raise a
:class:`NotImplementedError`, because ``np.put`` modifies its arguments in-place,
and in JAX arrays are immutable. A JAX-compatible approach to array updates
can be found in :attr:`jax.numpy.ndarray.at`.
""")
def put(*args, **kwargs):
  raise NotImplementedError(
    "jax.numpy.put is not implemented because JAX arrays cannot be modified in-place. "
    "For functional approaches to updating array values, see jax.numpy.ndarray.at: "
    "https://jax.readthedocs.io/en/latest/_autosummary/jax.numpy.ndarray.at.html.")
