def dtype(x: Any, *, canonicalize: bool = False) -> DType:
  """Return the dtype object for a value or type, optionally canonicalized based on X64 mode."""
  from jax._src import core     # TODO(frostig): break this cycle
  if x is None:
    raise ValueError(f"Invalid argument to dtype: {x}.")
  elif isinstance(x, type) and x in python_scalar_dtypes:
    dt = python_scalar_dtypes[x]
  elif type(x) in python_scalar_dtypes:
    dt = python_scalar_dtypes[type(x)]
  elif core.is_opaque_dtype(getattr(x, 'dtype', None)):
    dt = x.dtype
  else:
    dt = np.result_type(x)
  if dt not in _jax_dtype_set:
    raise TypeError(f"Value '{x}' with dtype {dt} is not a valid JAX array "
                    "type. Only arrays of numeric types are supported by JAX.")
  return canonicalize_dtype(dt) if canonicalize else dt
