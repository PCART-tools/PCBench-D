def _reshape(self: Array, *args: Any, order: str = "C") -> Array:
  """Returns an array containing the same data with a new shape.

  Refer to :func:`jax.numpy.reshape` for full documentation.
  """
  __tracebackhide__ = True
  newshape = _compute_newshape(self, args[0] if len(args) == 1 else args)
  if order == "C":
    return lax.reshape(self, newshape, None)
  elif order == "F":
    dims = list(range(self.ndim)[::-1])
    return lax.reshape(self, newshape[::-1], dims).T
  elif order == "A":
    raise NotImplementedError("np.reshape order=A is not implemented.")
  else:
    raise ValueError(f"Unexpected value for 'order' argument: {order}.")
