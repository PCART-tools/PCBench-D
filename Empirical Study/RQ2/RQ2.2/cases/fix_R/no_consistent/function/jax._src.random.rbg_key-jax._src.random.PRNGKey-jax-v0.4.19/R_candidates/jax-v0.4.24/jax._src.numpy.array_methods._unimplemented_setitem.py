def _unimplemented_setitem(self, i, x):
  msg = ("'{}' object does not support item assignment. JAX arrays are "
         "immutable. Instead of ``x[idx] = y``, use ``x = x.at[idx].set(y)`` "
         "or another .at[] method: "
         "https://jax.readthedocs.io/en/latest/_autosummary/jax.numpy.ndarray.at.html")
  raise TypeError(msg.format(type(self)))
