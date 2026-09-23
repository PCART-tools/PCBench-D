@profiler.annotate_function
def lower_xla_callable(fun: lu.WrappedFun, device, backend, name,
                       donated_invars, always_lower: bool, keep_unused: bool,
                       *arg_specs):
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
    abstract_args = [aval for aval, _ in fun.in_type]
  with log_elapsed_time(f"Finished tracing + transforming {fun.__name__} "
                        "for jit in {elapsed_time} sec"):
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
    logging.log(log_priority, msg)

  if nreps > 1:
    warnings.warn(
        f"The jitted function {name} includes a pmap. Using "
         "jit-of-pmap can lead to inefficient data movement, as the outer jit "
         "does not preserve sharded data representations and instead collects "
         "input and output arrays onto a single device. "
         "Consider removing the outer jit unless you know what you're doing. "
         "See https://github.com/google/jax/issues/2926.")

  if nreps > xb.device_count(backend):
    raise ValueError(
        f"compiling computation `{name}` that requires {nreps} replicas, but "
        f"only {xb.device_count(backend)} XLA devices are available.")

  if xb.process_count() > 1 and (nreps > 1 or
                                 jaxpr_has_primitive(jaxpr, "xla_pmap")):
    raise NotImplementedError(
        "jit of multi-host pmap not implemented (and jit-of-pmap can cause "
        "extra data movement anyway, so maybe you don't want it after all).")

  # pass long arg lists as tuple for TPU
  tuple_args = len(abstract_args) > 100
  axis_env = xla.AxisEnv(nreps, (), ())
  name_stack = util.new_name_stack(util.wrap_name(name, 'jit'))
  closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
  module_name = f"jit_{fun.__name__}"
  unordered_effects = [eff for eff in closed_jaxpr.effects
                       if eff not in core.ordered_effects]
  ordered_effects = [eff for eff in closed_jaxpr.effects
                     if eff in core.ordered_effects]
  lowering_result = mlir.lower_jaxpr_to_module(
      module_name, closed_jaxpr,
      unordered_effects, ordered_effects, backend.platform,
      mlir.ReplicaAxisContext(axis_env), name_stack, donated_invars)
  module, keepalive, host_callbacks = (
      lowering_result.module, lowering_result.keepalive,
      lowering_result.host_callbacks)
  return XlaComputation(
      name, module, False, donated_invars, fun.in_type, out_type, nreps=nreps,
      device=device, backend=backend, tuple_args=tuple_args,
      in_avals=abstract_args, out_avals=out_avals,
      has_unordered_effects=bool(unordered_effects),
      ordered_effects=ordered_effects, kept_var_idx=kept_var_idx,
      keepalive=keepalive, host_callbacks=host_callbacks)
