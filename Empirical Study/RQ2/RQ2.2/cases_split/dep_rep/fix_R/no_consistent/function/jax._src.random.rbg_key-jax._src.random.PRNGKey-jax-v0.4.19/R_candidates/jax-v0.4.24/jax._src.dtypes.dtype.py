def dtype(x: Any, *, canonicalize: bool = False) -> DType:
  """Return the dtype object for a value or type, optionally canonicalized based on X64 mode."""
  if x is None:
    raise ValueError(f"Invalid argument to dtype: {x}.")
  elif isinstance(x, type) and x in python_scalar_dtypes:
    dt = python_scalar_dtypes[x]
  elif type(x) in python_scalar_dtypes:
    dt = python_scalar_dtypes[type(x)]
  elif _issubclass(x, np.generic):
    return np.dtype(x)
  elif issubdtype(getattr(x, 'dtype', None), extended):
    dt = x.dtype
  else:
    try:
      dt = np.result_type(x)
    except TypeError as err:
      raise TypeError(f"Cannot determine dtype of {x}") from err
  if dt not in _jax_dtype_set and not issubdtype(dt, extended):
    raise TypeError(f"Value '{x}' with dtype {dt} is not a valid JAX array "
                    "type. Only arrays of numeric types are supported by JAX.")
  # TODO(jakevdp): fix return type annotation and remove this ignore.
  return canonicalize_dtype(dt, allow_extended_dtype=True) if canonicalize else dt  # type: ignore[return-value]
