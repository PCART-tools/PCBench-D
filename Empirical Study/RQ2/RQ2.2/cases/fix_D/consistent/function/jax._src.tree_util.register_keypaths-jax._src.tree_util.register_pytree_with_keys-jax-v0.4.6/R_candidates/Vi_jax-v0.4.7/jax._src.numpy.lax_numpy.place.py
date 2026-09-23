@util._wraps(np.place, lax_description="""
Numpy function :func:`numpy.place` is not available in JAX and will raise a
:class:`NotImplementedError`, because ``np.place`` modifies its arguments in-place,
and in JAX arrays are immutable. A JAX-compatible approach to array updates
can be found in :attr:`jax.numpy.ndarray.at`.
""")
def place(*args, **kwargs):
  raise NotImplementedError(
    "jax.numpy.place is not implemented because JAX arrays cannot be modified in-place. "
    "For functional approaches to updating array values, see jax.numpy.ndarray.at: "
    "https://jax.readthedocs.io/en/latest/_autosummary/jax.numpy.ndarray.at.html.")
