@profiler.annotate_function
def lower_sharding_computation(
    fun_or_jaxpr: lu.WrappedFun | core.ClosedJaxpr,
    api_name: str,
    fun_name: str,
    in_shardings: Sequence[MaybeSharding],
    out_shardings: Sequence[MaybeSharding] | UnspecifiedValue,
    donated_invars: Sequence[bool],
    global_in_avals: Sequence[core.ShapedArray],
    *,
    keep_unused: bool,
    inline: bool,
    always_lower: bool,
    devices_from_context: Sequence[xc.Device] | None = None,
    lowering_platform: str | None,
    override_lowering_rules: None | (
        tuple[tuple[core.Primitive, mlir.LoweringRule]]) = None,
) -> MeshComputation:
  """Lowers a computation to XLA. It can take arbitrary shardings as input.

  The caller of this code can pass in a singleton UNSPECIFIED because the
  number of out_avals might not be known at that time and
  lower_sharding_computation calculates the number of out_avals so it can apply
  the singleton UNSPECIFIED to all out_avals.
  """
  # 1. Trace to jaxpr and preprocess/verify it
  auto_spmd_lowering = (
      check_if_any_auto(in_shardings) if is_unspecified(out_shardings) else
      check_if_any_auto(it.chain.from_iterable([in_shardings, out_shardings])))  # type: ignore

  (closed_jaxpr, global_in_avals, global_out_avals, donated_invars,
   kept_var_idx, name_stack) = _trace_to_jaxpr_and_dce(
      fun_or_jaxpr, global_in_avals, api_name, fun_name, keep_unused,
      donated_invars, auto_spmd_lowering)
  jaxpr = closed_jaxpr.jaxpr
  in_shardings = tuple(s for i, s in enumerate(in_shardings) if i in kept_var_idx)

  if is_unspecified(out_shardings):
    out_shardings = (UNSPECIFIED,) * len(global_out_avals)
  assert isinstance(out_shardings, tuple)
  assert len(out_shardings) == len(global_out_avals), (
      len(out_shardings), len(global_out_avals))

  # Device assignment across all inputs, outputs and shardings inside jaxpr
  # should be the same.
  jaxpr_sharding = list(dispatch.jaxpr_shardings(jaxpr))
  backend, device_assignment = _get_and_check_device_assignment(
      it.chain([(i, MismatchType.ARG_SHARDING, None) for i in in_shardings],
               [(o, MismatchType.OUT_SHARDING, None) for o in out_shardings],
               [(js, MismatchType.SHARDING_INSIDE_COMPUTATION, source_info)
                for js, source_info in jaxpr_sharding]),
      devices_from_context)

  committed = bool(
      devices_from_context or
      len(device_assignment) > 1 or
      any(not is_unspecified(i) for i in in_shardings) or
      any(not is_unspecified(js) for js, _ in jaxpr_sharding) or
      any(not is_unspecified(o) for o in out_shardings))

  gs = sharding_impls.GSPMDSharding.get_replicated(device_assignment)
  in_shardings = tuple(gs if is_unspecified(i) else i for i in in_shardings)

  da_object = _create_da_object(tuple(device_assignment))

  if not da_object.is_fully_addressable:
    check_multihost_collective_allowlist(jaxpr)
    if inline and config.jax_spmd_mode != 'allow_all':
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
  kept_outputs = [True] * len(global_out_avals)

  # Computations that only produce constants and/or only rearrange their inputs,
  # which are often produced from partial evaluation, don't need compilation,
  # and don't need to evaluate their arguments.
  if (not always_lower and not (jaxpr.effects or has_outfeed) and
      (not jaxpr.eqns and all(kept_outputs) or not jaxpr.outvars) and
      all(is_unspecified(o) for o in out_shardings)):
    return MeshComputation(
        str(name_stack), None, True, donated_invars, jaxpr=jaxpr,
        consts=closed_jaxpr.consts, global_in_avals=global_in_avals,
        global_out_avals=global_out_avals, in_shardings=in_shardings,
        backend=backend, da_object=da_object,
        committed=committed, kept_var_idx=kept_var_idx, keepalive=None)

  # 2. Build up the HLO
  semantic_in_shardings = SemanticallyEqualShardings(in_shardings)  # type: ignore
  semantic_out_shardings = SemanticallyEqualShardings(out_shardings)
  (module, keepalive, host_callbacks, unordered_effects, ordered_effects,
   nreps, tuple_args, shape_poly_state) = _cached_lowering_to_hlo(
       closed_jaxpr, api_name, fun_name, backend, semantic_in_shardings,
       semantic_out_shardings, da_object, lowering_platform,
       donated_invars, name_stack, override_lowering_rules)

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
      global_in_avals=global_in_avals,
      global_out_avals=global_out_avals,
      in_shardings=in_shardings,
      out_shardings=out_shardings,
      spmd_lowering=True,
      tuple_args=tuple_args,
      auto_spmd_lowering=auto_spmd_lowering,
      unordered_effects=unordered_effects,
      ordered_effects=ordered_effects,
      host_callbacks=host_callbacks,
      keepalive=keepalive,
      kept_var_idx=kept_var_idx,
      backend=backend,
      device_assignment=da_object,
      committed=committed,
      pmap_nreps=nreps,
      jaxpr_debug_info=closed_jaxpr.jaxpr.debug_info,
      shape_poly_state=shape_poly_state)
