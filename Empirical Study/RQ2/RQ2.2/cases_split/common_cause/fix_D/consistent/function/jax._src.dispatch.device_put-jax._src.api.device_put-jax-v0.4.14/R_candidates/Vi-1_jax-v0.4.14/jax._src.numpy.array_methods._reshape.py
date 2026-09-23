def _reshape(a: Array, *args: Any, order: str = "C") -> Array:
  """Returns an array containing the same data with a new shape.

  Refer to :func:`jax.numpy.reshape` for full documentation.
  """
  newshape = _compute_newshape(a, args[0] if len(args) == 1 else args)
  if order == "C":
    return lax.reshape(a, newshape, None)
  elif order == "F":
    dims = list(range(a.ndim)[::-1])
    return lax.reshape(a, newshape[::-1], dims).T
  elif order == "A":
    raise NotImplementedError("np.reshape order=A is not implemented.")
  else:
    raise ValueError(f"Unexpected value for 'order' argument: {order}.")
