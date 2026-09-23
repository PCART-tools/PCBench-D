def _pjit_call_impl(*args, jaxpr,
                    in_shardings, out_shardings, resource_env,
                    donated_invars, name, keep_unused, inline):
  global _most_recent_pjit_call_executable

  in_shardings = _resolve_in_shardings(
      args, in_shardings, out_shardings,
      resource_env.physical_mesh if resource_env is not None else None)

  _allow_propagation_to_outputs = [_is_unspecified(o) for o in out_shardings]
  compiled = _pjit_lower(
      jaxpr, in_shardings, out_shardings, resource_env,
      donated_invars, name, keep_unused,
      always_lower=False, lowering_platform=None).compile(
          _allow_propagation_to_outputs=_allow_propagation_to_outputs)
  _most_recent_pjit_call_executable.value = compiled
  # This check is expensive so only do it if enable_checks is on.
  if compiled._auto_spmd_lowering and config.jax_enable_checks:
    pxla.check_gda_or_array_xla_sharding_match(args, compiled._in_shardings)
  if config.jax_distributed_debug:
    # Defensively only perform fingerprint logic if debug logging is enabled
    # NOTE(skyewm): I didn't benchmark this
    fingerprint = None
    if hasattr(compiled.runtime_executable(), "fingerprint"):
      fingerprint = compiled.runtime_executable().fingerprint
    if fingerprint is not None:
      fingerprint = fingerprint.hex()
    distributed_debug_log(("Running pjit'd function", name),
                          ("in_shardings", in_shardings),
                          ("out_shardings", out_shardings),
                          ("abstract args", map(xla.abstractify, args)),
                          ("fingerprint", fingerprint))
  try:
    return compiled.unsafe_call(*args)
  except FloatingPointError:
    assert config.jax_debug_nans or config.jax_debug_infs  # compiled_fun can only raise in this case

    _ = core.jaxpr_as_fun(jaxpr)(*args)  # may raise, not return

    # If control reaches this line, we got a NaN on the output of `compiled`
    # but not `fun.call_wrapped` on the same arguments. Let's tell the user.
    msg = ("An invalid value was encountered in the output of the "
           f"`jit`-decorated function {name}. Because "
           "config.jax_debug_nans and/or config.jax_debug_infs is set, the "
           "de-optimized function (i.e., the function as if the `jit` "
           "decorator were removed) was called in an attempt to get a more "
           "precise error message. However, the de-optimized function did not "
           "produce invalid values during its execution. This behavior can "
           "result from `jit` optimizations causing the invalid value to be "
           "produced. It may also arise from having nan/inf constants as "
           "outputs, like `jax.jit(lambda ...: jax.numpy.nan)(...)`. "
           "\n\n"
           "It may be possible to avoid the invalid value by removing the "
           "`jit` decorator, at the cost of losing optimizations. "
           "\n\n"
           "If you see this error, consider opening a bug report at "
           "https://github.com/google/jax.")
    raise FloatingPointError(msg)
