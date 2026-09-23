def _pjit_call_impl_python(
    *args, jaxpr, in_shardings, out_shardings, resource_env, donated_invars,
    name, keep_unused, inline):
  global _most_recent_pjit_call_executable

  in_shardings = _resolve_in_shardings(
      args, in_shardings, out_shardings,
      resource_env.physical_mesh if resource_env is not None else None)

  compiled = _pjit_lower(
      jaxpr, in_shardings, out_shardings, resource_env,
      donated_invars, name, keep_unused, inline,
      lowering_parameters=mlir.LoweringParameters()).compile()
  _most_recent_pjit_call_executable.weak_key_dict[jaxpr] = compiled
  # This check is expensive so only do it if enable_checks is on.
  if compiled._auto_spmd_lowering and config.enable_checks.value:
    pxla.check_gda_or_array_xla_sharding_match(args, compiled._in_shardings,
                                               jaxpr.jaxpr.debug_info)
  if config.distributed_debug.value:
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
    return compiled.unsafe_call(*args), compiled
  except FloatingPointError as e:
    assert config.debug_nans.value or config.debug_infs.value  # compiled_fun can only raise in this case

    if len(jaxpr.eqns) > 1:
      _ = core.jaxpr_as_fun(jaxpr)(*args)  # may raise, not return

    # If control reaches this line, we got a NaN on the output of `compiled`
    # but not `fun.call_wrapped` on the same arguments. Let's tell the user.
    msg = (f"{str(e)}. Because "
           "jax_config.debug_nans.value and/or config.jax_debug_infs is set, the "
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
