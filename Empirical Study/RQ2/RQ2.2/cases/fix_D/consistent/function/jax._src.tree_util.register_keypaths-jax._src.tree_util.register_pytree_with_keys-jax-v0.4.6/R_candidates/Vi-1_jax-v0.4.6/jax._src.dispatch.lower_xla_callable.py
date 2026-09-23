@profiler.annotate_function
def lower_xla_callable(
    fun: lu.WrappedFun, device, backend, name, donated_invars,
    always_lower: bool, keep_unused: bool, *arg_specs,
    lowering_platform: Optional[str]):
  """Lower into XLA.

  Args:
    always_lower: If `True`, even trivial programs (not doing any computation
      such as lambda x: x) will be lowered into an XLA program.
    keep_unused: If `False` (the default), arguments that JAX determines to be
      unused by `fun` *may* be dropped from resulting compiled XLA executables.
      Such arguments will not be transferred to the device nor provided to the
      underlying executable. If `True`, unused arguments will not be pruned.
  """
  if device is not None and backend is not None:
    raise ValueError("can't specify both a device and a backend for jit, "
                     "got device={} and backend={}".format(device, backend))
  abstract_args, arg_devices = util.unzip2(arg_specs)
  if fun.in_type is None:
    # Add an annotation inferred from the arguments; no dynamic axes here.
    in_type = tuple(unsafe_zip(abstract_args, itertools.repeat(True)))
    fun = lu.annotate(fun, in_type)
  else:
    assert abstract_args == (None,) * len(abstract_args)
    abstract_args = tuple(aval for aval, _ in fun.in_type)

  with log_elapsed_time(f"Finished tracing + transforming {fun.__name__} "
                        "for jit in {elapsed_time} sec",
                        event=JAXPR_TRACE_EVENT):
    jaxpr, out_type, consts = pe.trace_to_jaxpr_final2(
        fun, pe.debug_info_final(fun, "jit"))
  out_avals, kept_outputs = util.unzip2(out_type)

  if any(isinstance(c, core.Tracer) for c in consts):
    raise UnexpectedTracerError("Encountered an unexpected tracer.")

  if config.jax_dynamic_shapes:
    keep_unused = True
    has_outfeed = False
    donated_invars = [False] * len(fun.in_type)
  else:
    has_outfeed = core.jaxpr_uses_outfeed(jaxpr)
    jaxpr = apply_outfeed_rewriter(jaxpr)

  if not keep_unused:
    jaxpr, kept_const_idx, kept_var_idx = _prune_unused_inputs(jaxpr)
    consts = [c for i, c in enumerate(consts) if i in kept_const_idx]
    abstract_args, arg_devices = util.unzip2(
        [a for i, a in enumerate(arg_specs) if i in kept_var_idx])
    donated_invars = [x for i, x in enumerate(donated_invars)
                      if i in kept_var_idx]
    del kept_const_idx
  else:
    kept_var_idx = set(range(len(fun.in_type)))

  nreps = jaxpr_replicas(jaxpr)
  device = _xla_callable_device(nreps, backend, device, arg_devices)
  backend = xb.get_device_backend(device) if device else xb.get_backend(backend)

  if config.jax_dynamic_shapes and jaxpr_has_bints(jaxpr):
    jaxpr, consts = pe.pad_jaxpr(jaxpr, consts)

  map(prefetch, itertools.chain(consts, jaxpr_literals(jaxpr)))

  # Computations that only produce constants and/or only rearrange their inputs,
  # which are often produced from partial evaluation, don't need compilation,
  # and don't need to evaluate their arguments.
  if (not always_lower and not (jaxpr.effects or has_outfeed) and
      (not jaxpr.eqns and all(kept_outputs) or not jaxpr.outvars)):
    return XlaComputation(
        name, None, True, None, None, None, jaxpr=jaxpr, consts=consts,
        device=device, in_avals=abstract_args, out_avals=out_avals,
        has_unordered_effects=False, ordered_effects=[],
        kept_var_idx=kept_var_idx, keepalive=None, host_callbacks=[])

  if not _on_exit:
    log_priority = logging.WARNING if config.jax_log_compiles else logging.DEBUG
    if len(abstract_args) > 10:
      msg = f"Compiling {fun.__name__} ({id(fun)}) for {len(abstract_args)} args."
    else:
      msg = f"Compiling {fun.__name__} ({id(fun)} for args {abstract_args}."
    logger.log(log_priority, msg)

  raise_warnings_or_errors_for_jit_of_pmap(nreps, backend, name, jaxpr)

  # pass long arg lists as tuple for TPU
  tuple_args = should_tuple_args(len(abstract_args), backend.platform)
  axis_env = xla.AxisEnv(nreps, (), ())
  name_stack = source_info_util.new_name_stack(util.wrap_name(name, 'jit'))
  closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
  closed_out_type = [
      (a.update(shape=tuple(pe.InDBIdx(d.val - len(consts))
                            if type(d) is pe.InDBIdx else d for d in a.shape))
       if type(a) is core.DShapedArray else a, b) for a, b in out_type]
  module_name = f"jit_{fun.__name__}"
  unordered_effects = list(
    effects.ordered_effects.filter_not_in(closed_jaxpr.effects))
  ordered_effects = list(
    effects.ordered_effects.filter_in(closed_jaxpr.effects))
  lowering_result = mlir.lower_jaxpr_to_module(
      module_name, closed_jaxpr, unordered_effects,
      ordered_effects, backend,
      lowering_platform or backend.platform,
      mlir.ReplicaAxisContext(axis_env), name_stack, donated_invars)
  module, keepalive, host_callbacks = (
      lowering_result.module, lowering_result.keepalive,
      lowering_result.host_callbacks)
  return XlaComputation(
      name, module, False, donated_invars, fun.in_type, tuple(closed_out_type),
      nreps=nreps, device=device, backend=backend, tuple_args=tuple_args,
      in_avals=abstract_args, out_avals=out_avals,
      has_unordered_effects=bool(unordered_effects),
      ordered_effects=ordered_effects, kept_var_idx=kept_var_idx,
      keepalive=keepalive, host_callbacks=host_callbacks)
