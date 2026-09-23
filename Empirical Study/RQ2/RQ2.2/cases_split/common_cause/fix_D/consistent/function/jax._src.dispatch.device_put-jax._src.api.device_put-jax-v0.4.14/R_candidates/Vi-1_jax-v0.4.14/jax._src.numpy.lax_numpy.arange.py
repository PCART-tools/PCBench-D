@util._wraps(np.arange)
def arange(start: DimSize, stop: Optional[DimSize] = None,
           step: Optional[DimSize] = None, dtype: Optional[DTypeLike] = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "arange")
  if not jax.config.jax_dynamic_shapes:
    util.check_arraylike("arange", start)
    if stop is None and step is None:
      start = core.concrete_or_error(None, start, "It arose in the jnp.arange argument 'stop'")
    else:
      start = core.concrete_or_error(None, start, "It arose in the jnp.arange argument 'start'")
  util.check_arraylike_or_none("arange", None, stop, step)
  stop = core.concrete_or_error(None, stop, "It arose in the jnp.arange argument 'stop'")
  step = core.concrete_or_error(None, step, "It arose in the jnp.arange argument 'step'")
  start_name = "stop" if stop is None and step is None else "start"
  for name, val in [(start_name, start), ("stop", stop), ("step", step)]:
    if val is not None and np.ndim(val) != 0:
      raise ValueError(f"jax.numpy.arange: arguments must be scalars; got {name}={val}")
  if any(core.is_symbolic_dim(v) for v in (start, stop, step)):
    # Some dynamic shapes
    if stop is None and step is None:
      stop = start
      start = 0
      step = 1
    elif stop is not None and step is None:
      step = 1
    return _arange_dynamic(start, stop, step, dtype or dtypes.canonicalize_dtype(np.int64))
  if dtype is None:
    dtype = result_type(start, *(x for x in [stop, step] if x is not None))
  dtype = _jnp_dtype(dtype)
  if stop is None and step is None:
    start_dtype = _dtype(start)
    if (not dtypes.issubdtype(start_dtype, np.integer) and
        not dtypes.issubdtype(start_dtype, dtypes.extended)):
      ceil_ = ufuncs.ceil if isinstance(start, core.Tracer) else np.ceil
      start = ceil_(start).astype(int)  # type: ignore
    return lax.iota(dtype, start)
  else:
    if step is None and start == 0 and stop is not None:
      stop = np.ceil(stop).astype(int)
      return lax.iota(dtype, stop)
    return array(np.arange(start, stop=stop, step=step, dtype=dtype))
