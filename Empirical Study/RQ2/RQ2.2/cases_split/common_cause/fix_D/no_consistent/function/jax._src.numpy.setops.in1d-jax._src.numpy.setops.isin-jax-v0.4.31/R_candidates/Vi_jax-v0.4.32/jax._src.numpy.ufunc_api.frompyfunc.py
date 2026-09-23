def frompyfunc(func: Callable[..., Any], /, nin: int, nout: int,
               *, identity: Any = None) -> ufunc:
  """Create a JAX ufunc from an arbitrary JAX-compatible scalar function.

  Args:
    func : a callable that takes `nin` scalar arguments and returns `nout` outputs.
    nin: integer specifying the number of scalar inputs
    nout: integer specifying the number of scalar outputs
    identity: (optional) a scalar specifying the identity of the operation, if any.

  Returns:
    wrapped : jax.numpy.ufunc wrapper of func.
  """
  return ufunc(func, nin, nout, identity=identity)
