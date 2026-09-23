def _reshape(a, *args, order="C"):
  newshape = _compute_newshape(a, args[0] if len(args) == 1 else args)
  if order == "C":
    return lax.reshape(a, newshape, None)
  elif order == "F":
    dims = np.arange(ndim(a))[::-1]
    return lax.reshape(a, newshape[::-1], dims).T
  elif order == "A":
    raise NotImplementedError("np.reshape order=A is not implemented.")
  else:
    raise ValueError(f"Unexpected value for 'order' argument: {order}.")
