@profiler.annotate_function
def lower_sharding_computation(
    fun_or_jaxpr: Union[lu.WrappedFun, core.ClosedJaxpr],
    api_name: str,
    fun_name: str,
    in_shardings: Sequence[Union[sharding_impls.XLACompatibleSharding, UnspecifiedValue]],
    out_shardings: Union[Sequence[Union[sharding_impls.XLACompatibleSharding, UnspecifiedValue]], UnspecifiedValue],
    donated_invars: Sequence[bool],
    global_in_avals: Sequence[core.ShapedArray],
    *,
    keep_unused: bool,
    always_lower: bool,
    devices_from_context: Optional[Sequence[xc.Device]] = None,
    lowering_platform: Optional[str],
) -> MeshComputation:
  """Lowers a computation to XLA. It can take arbitrary shardings as input.

  The caller of this code can pass in a singleton _UNSPECIFIED because the
  number of out_avals might not be known at that time and
  lower_sharding_computation calculates the number of out_avals so it can apply
  the singleton _UNSPECIFIED to all out_avals.
  """
  # 1. Trace to jaxpr and preprocess/verify it
  name_stack = source_info_util.new_name_stack(wrap_name(fun_name, api_name))

  if isinstance(fun_or_jaxpr, lu.WrappedFun):
    with dispatch.log_elapsed_time(f"Finished tracing + transforming {name_stack} "
                                  "in {elapsed_time} sec",
                                  event=dispatch.JAXPR_TRACE_EVENT):
      jaxpr, global_out_avals, consts = pe.trace_to_jaxpr_final(
          fun_or_jaxpr, global_in_avals)
  else:
    assert isinstance(fun_or_jaxpr, core.ClosedJaxpr)
    jaxpr = fun_or_jaxpr.jaxpr
    global_out_avals = fun_or_jaxpr.out_avals
    consts = fun_or_jaxpr.consts

  kept_outputs = [True] * len(global_out_avals)

  if _is_unspecified(out_shardings):
    out_shardings = (_UNSPECIFIED,) * len(global_out_avals)
  # mypy doesn't understand that out_sharding here is always a sequence.
  assert len(out_shardings) == len(global_out_avals), (  # type: ignore
      len(out_shardings), len(global_out_avals))  # type: ignore

  # Device assignment across all inputs, outputs and shardings inside jaxpr
  # should be the same.
  jaxpr_sharding = list(dispatch.jaxpr_shardings(jaxpr))
  backend, device_assignment = _get_and_check_device_assignment(
      it.chain([(i, MismatchType.ARG_SHARDING, None) for i in in_shardings],
               [(o, MismatchType.OUT_SHARDING, None) for o in out_shardings],  # type: ignore
               [(js, MismatchType.SHARDING_INSIDE_COMPUTATION, source_info)  # type: ignore
                for js, source_info in jaxpr_sharding]),
      devices_from_context)

  # TODO(yashkatariya): Make this logic work after DCE because there can be
  # equations inside the jaxpr that don't affect the output so whether the
  # output(s) are committed or not should not depend on it.
  committed = bool(
      devices_from_context or
      len(device_assignment) > 1 or
      any(not _is_unspecified(i) for i in in_shardings) or
      any(not _is_unspecified(js) for js, _ in jaxpr_sharding) or  # type: ignore
      any(not _is_unspecified(o) for o in out_shardings))  # type: ignore

  in_shardings = tuple(sharding_impls.GSPMDSharding.get_replicated(device_assignment)
                       if _is_unspecified(i) else i for i in in_shardings)

  log_priority = logging.WARNING if config.jax_log_compiles else logging.DEBUG
  logger.log(log_priority,
              "Compiling %s for with global shapes and types %s. "
              "Argument mapping: %s.",
              fun_name, global_in_avals, in_shardings)

  if keep_unused or any(hasattr(a, "shape") and not core.is_constant_shape(a.shape)
                        for a in global_in_avals):
    kept_var_idx = set(range(len(global_in_avals)))
  else:
    jaxpr, kept_const_idx, kept_var_idx = dispatch._prune_unused_inputs(jaxpr)
    consts = [c for i, c in enumerate(consts) if i in kept_const_idx]
    global_in_avals = tuple(a for i, a in enumerate(global_in_avals) if i in kept_var_idx)
    in_shardings = tuple(s for i, s in enumerate(in_shardings) if i in kept_var_idx)
    donated_invars = tuple(x for i, x in enumerate(donated_invars) if i in kept_var_idx)
    del kept_const_idx

  local_device_assignment = [d for d in device_assignment
                             if d.process_index == d.client.process_index()]
  if len(device_assignment) != len(local_device_assignment):
    check_multihost_collective_allowlist(jaxpr)
    # TODO(yashkatariya): Once jit and pjit's frontend is merged, use the
    # argument on jit `_allow_multiprocess` (which will be added later) instead
    # of the `api_name` check here.
    # Furthermore, `allow_jit` is not allowed yet because `allow_jit` only
    # allows explicit `jax.jit` to work but not implicitly jitted `jnp`.
    # operations. This restriction will be relaxed in the future when the
    # default value of `spmd_mode` config changes to `allow_jit`.
    if api_name == 'jit' and config.jax_spmd_mode != 'allow_all':
      raise RuntimeError(
          "Running operations on `Array`s that are not fully addressable by this "
          "process (i.e. `Array`s with data sharded across multiple devices and "
          "processes.) is dangerous. It’s very important that all processes run "
          "the same cross-process computations in the same order otherwise it "
          "can lead to hangs. "
          "If you’re not already familiar with JAX’s multi-process "
          "programming model, please read "
          "https://jax.readthedocs.io/en/latest/multi_process.html. "
          "To fix this error, run your `jitted` computation inside "
          "`with jax.spmd_mode('allow_all'):` context manager.")

  has_outfeed = core.jaxpr_uses_outfeed(jaxpr)
  jaxpr = dispatch.apply_outfeed_rewriter(jaxpr)

  # Computations that only produce constants and/or only rearrange their inputs,
  # which are often produced from partial evaluation, don't need compilation,
  # and don't need to evaluate their arguments.
  if (not always_lower and not (jaxpr.effects or has_outfeed) and
      (not jaxpr.eqns and all(kept_outputs) or not jaxpr.outvars) and
      all(_is_unspecified(o) for o in out_shardings)):  # type: ignore
    return MeshComputation(
        str(name_stack), None, True, donated_invars, jaxpr=jaxpr, consts=consts,
        global_in_avals=global_in_avals, global_out_avals=global_out_avals,
        in_shardings=in_shardings, backend=backend,
        device_assignment=device_assignment, committed=committed,
        kept_var_idx=kept_var_idx, keepalive=None)

  # Look at the number of replcas present in the jaxpr. In
  # lower_sharding_computation, nreps > 1 during `jit(pmap)` cases. This is
  # handled here so as to deprecate the lower_xla_callable codepath when
  # `jax.Array` is turned on by default.
  # TODO(yashkatariya): Remove this when `jit(pmap)` is removed.
  nreps = dispatch.jaxpr_replicas(jaxpr)
  dispatch.raise_warnings_or_errors_for_jit_of_pmap(nreps, backend, fun_name, jaxpr)

  # 2. Build up the HLO
  tuple_args = dispatch.should_tuple_args(len(global_in_avals), backend.platform)

  in_op_shardings: Optional[List[Optional[xc.OpSharding]]]
  out_op_shardings: Optional[List[Optional[xc.OpSharding]]]
  axis_ctx: mlir.AxisContext

  if nreps == 1:
    in_op_shardings = []
    for aval, i in safe_zip(global_in_avals, in_shardings):
      if aval is core.abstract_token:
        in_op_shardings.append(None)
      elif core.is_opaque_dtype(aval.dtype):
        in_op_shardings.append(aval.dtype._rules.physical_op_sharding(aval, i))
      else:
        in_op_shardings.append(i._to_xla_op_sharding(aval.ndim))  # type: ignore[union-attr]

    # TODO(yashkatariya): Fix the HLO produced if out_partitions is
    # [None, OpShardingProto] has the sharding annotations.
    out_op_shardings = []
    for aval, o in safe_zip(global_out_avals, out_shardings):  # type: ignore[arg-type]
      if _is_unspecified(o) or aval is core.abstract_token:
        out_op_shardings.append(None)
      elif core.is_opaque_dtype(aval.dtype):
        out_op_shardings.append(aval.dtype._rules.physical_op_sharding(aval, o))
      else:
        out_op_shardings.append(o._to_xla_op_sharding(aval.ndim))  # type: ignore[union-attr]
    replicated_args = [False] * len(global_in_avals)
    axis_ctx = mlir.ShardingContext(device_assignment)
  else:
    # This path is triggered for `jit(pmap)` cases.
    replicated_args = None
    in_op_shardings = None
    out_op_shardings = None
    axis_env = xla.AxisEnv(nreps, (), ())
    axis_ctx = mlir.ReplicaAxisContext(axis_env)

  closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
  module_name = f"{api_name}_{fun_name}"

  if len(device_assignment) > 1:
    if any(effects.ordered_effects.contains(eff) for eff
           in closed_jaxpr.effects):
      raise ValueError("Ordered effects are not supported for more than 1 device.")
  unordered_effects = list(
      effects.ordered_effects.filter_not_in(closed_jaxpr.effects))
  ordered_effects = list(effects.ordered_effects.filter_in(closed_jaxpr.effects))
  lowering_result = mlir.lower_jaxpr_to_module(
      module_name,
      closed_jaxpr,
      unordered_effects,
      ordered_effects,
      backend,
      # Optionally, override the lowering platform
      lowering_platform or backend.platform,
      axis_ctx,
      name_stack,
      donated_invars,
      replicated_args=replicated_args,
      arg_shardings=in_op_shardings,
      result_shardings=out_op_shardings,
      arg_names=jaxpr.debug_info and jaxpr.debug_info.arg_names,
      result_names=jaxpr.debug_info and jaxpr.debug_info.result_paths)

  module, keepalive, host_callbacks = (
      lowering_result.module, lowering_result.keepalive,
      lowering_result.host_callbacks)

  # backend and device_assignment is passed through to MeshExecutable because
  # if keep_unused=False and all in_shardings are pruned, then there is no way
  # to get the device_assignment and backend. So pass it to MeshExecutable
  # because we calculate the device_assignment and backend before in_shardings,
  # etc are pruned.
  return MeshComputation(
      str(name_stack),
      module,
      False,
      donated_invars,
      mesh=None,
      global_in_avals=global_in_avals,
      global_out_avals=global_out_avals,
      in_shardings=in_shardings,
      out_shardings=out_shardings,
      spmd_lowering=True,
      tuple_args=tuple_args,
      auto_spmd_lowering=False,
      unordered_effects=unordered_effects,
      ordered_effects=ordered_effects,
      host_callbacks=host_callbacks,
      keepalive=keepalive,
      kept_var_idx=kept_var_idx,
      backend=backend,
      device_assignment=device_assignment,
      committed=committed,
      pmap_nreps=nreps)
