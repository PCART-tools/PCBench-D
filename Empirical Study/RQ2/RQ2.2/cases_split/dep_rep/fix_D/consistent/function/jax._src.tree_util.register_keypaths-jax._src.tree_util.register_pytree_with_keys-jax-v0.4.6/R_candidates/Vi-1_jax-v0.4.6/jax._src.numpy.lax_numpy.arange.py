@util._wraps(np.arange)
def arange(start: DimSize, stop: Optional[DimSize] = None,
           step: Optional[DimSize] = None, dtype: Optional[DTypeLike] = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "arange")
  require = partial(core.concrete_or_error, None)
  msg = "It arose in jax.numpy.arange argument `{}`.".format
  if _any(core.is_special_dim_size(d) for d in (start, stop, step)):
    if stop is not None or step is not None:
      raise ValueError(
          "jax.numpy.arange supports non-constant arguments only in "
          "single-argument form. Found "
          f"jax.numpy.arange({start=}, {stop=}, {step=})")
    return lax.iota(dtype or int_, start)
  if dtype is None:
    dtype = result_type(start, *(x for x in [stop, step] if x is not None))
  dtype = _jnp_dtype(dtype)
  if stop is None and step is None:
    start_dtype = _dtype(start)
    if not jax.config.jax_dynamic_shapes:
      start = require(start, msg("stop"))
    if (not dtypes.issubdtype(start_dtype, np.integer) and
        not core.is_opaque_dtype(start_dtype)):
      ceil_ = ufuncs.ceil if isinstance(start, core.Tracer) else np.ceil
      start = ceil_(start).astype(int)  # type: ignore
    return lax.iota(dtype, start)
  else:
    start = require(start, msg("start"))
    stop = None if stop is None else require(stop, msg("stop"))
    step = None if step is None else require(step, msg("step"))
    if step is None and start == 0 and stop is not None:
      stop = np.ceil(stop).astype(int)
      return lax.iota(dtype, stop)
    return array(np.arange(start, stop=stop, step=step, dtype=dtype))
