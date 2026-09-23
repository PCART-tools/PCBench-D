@_wraps(np.take, skip_params=['out'], lax_description="""\
In the JAX version, the ``mode`` argument defaults to a special mode
(``"fill"``) that returns invalid values (e.g., NaN) for out-of-bounds indices.
See :attr:`jax.numpy.ndarray.at` for more discussion of out-of-bounds indexing
in JAX.
""")
def take(a, indices, axis: Optional[int] = None, out=None, mode=None):
  return _take(a, indices, None if axis is None else operator.index(axis), out,
               mode)
