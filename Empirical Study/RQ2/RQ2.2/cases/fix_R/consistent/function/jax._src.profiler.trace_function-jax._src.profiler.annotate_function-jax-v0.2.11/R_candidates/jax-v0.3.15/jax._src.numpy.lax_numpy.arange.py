@_wraps(np.arange)
def arange(start: core.DimSize, stop: Optional[core.DimSize]=None,
           step: Optional[core.DimSize]=None, dtype=None):
  lax_internal._check_user_dtype_supported(dtype, "arange")
  require = partial(core.concrete_or_error, None)
  msg = "It arose in jax.numpy.arange argument `{}`.".format
  if _any(core.is_special_dim_size(d) for d in (start, stop, step)):
    if stop is not None or step is not None:
      raise ValueError(
          "jax.numpy.arange supports non-constant arguments only in single-argument form. "
          f"Found jax.numpy.arange(start={start}, stop={stop}, step={step})")
    return lax.iota(dtype or int_, start)
  if dtype is None:
    dtype = result_type(start, *(x for x in [stop, step] if x is not None))
  dtype = _jnp_dtype(dtype)
  if stop is None and step is None:
    if (jax.config.jax_dynamic_shapes and
        not isinstance(core.get_aval(start), core.AbstractBInt) and
        not isinstance(core.get_aval(start), core.ConcreteArray)):
      start = ceil(start).astype(int)  # note using jnp here
    elif (isinstance(start, core.BInt) or isinstance(start, core.Tracer) and
          isinstance(core.get_aval(start), core.AbstractBInt)):
      pass
    else:
      start = require(start, msg("stop"))
      start = np.ceil(start).astype(int)
    return lax.iota(dtype, start)
  else:
    start = require(start, msg("start"))
    stop = None if stop is None else require(stop, msg("stop"))
    step = None if step is None else require(step, msg("step"))
    if step is None and start == 0 and stop is not None:
      stop = np.ceil(stop).astype(int)
      return lax.iota(dtype, stop)
    return array(np.arange(start, stop=stop, step=step, dtype=dtype))
