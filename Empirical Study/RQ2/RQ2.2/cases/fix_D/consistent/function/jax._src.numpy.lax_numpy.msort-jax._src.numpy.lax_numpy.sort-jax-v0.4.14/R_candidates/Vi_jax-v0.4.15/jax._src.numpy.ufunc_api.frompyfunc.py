def frompyfunc(func, /, nin, nout, *, identity=None):
  """Create a JAX ufunc from an arbitrary JAX-compatible scalar function.

  Args:
    func : a callable that takes `nin` scalar arguments and return `nout` outputs.
    nin: integer specifying the number of scalar inputs
    nout: integer specifying the number of scalar outputs
    identity: (optional) a scalar specifying the identity of the operation, if any.

  Returns:
    wrapped : jax.numpy.ufunc wrapper of func.
  """
  # TODO(jakevdp): use functools.wraps or similar to wrap the docstring?
  return ufunc(func, nin, nout, identity=identity)
