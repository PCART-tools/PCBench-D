def lower_jaxpr_to_module(
    module_name: str,
    jaxpr: core.ClosedJaxpr,
    ordered_effects: list[core.Effect],
    backend_or_name: str | xb.XlaBackend | None,
    platform: str,
    axis_context: AxisContext,
    name_stack: source_info_util.NameStack,
    donated_args: Sequence[bool],
    replicated_args: Sequence[bool] | None = None,
    arg_shardings: Sequence[XLACompatibleSharding | None] | None = None,
    result_shardings: Sequence[XLACompatibleSharding | None] | None = None,
    arg_names: Sequence[str | None] | None = None,
    result_names: Sequence[str | None] | None = None,
    num_replicas: int = 1,
    num_partitions: int = 1,
    override_lowering_rules: None | (
        tuple[tuple[core.Primitive, LoweringRule]]) = None,
) -> LoweringResult:
  """Lowers a top-level jaxpr to an MLIR module.

  Handles the quirks of the argument/return value passing conventions of the
  runtime.
  """
  platform = xb.canonicalize_platform(platform)
  if not xb.is_known_platform(platform):
    raise ValueError(f"Unknown platform {platform}")
  input_output_aliases = None
  in_avals = (jaxpr.in_avals if arg_shardings is None else
              map(sharded_aval, jaxpr.in_avals, arg_shardings))
  out_avals = (jaxpr.out_avals if result_shardings is None else
               map(sharded_aval, jaxpr.out_avals, result_shardings))
  if platform in _platforms_with_donation:
    input_output_aliases, donated_args = _set_up_aliases(
        in_avals, out_avals, donated_args)
  unlowerable_effects = lowerable_effects.filter_not_in(jaxpr.effects)
  if unlowerable_effects:
    raise ValueError(f'Cannot lower jaxpr with effects: {jaxpr.effects}')
  if any(donated_args):
    unused_donations = [str(a) for a, d in zip(in_avals, donated_args) if d]
    msg = "See an explanation at https://jax.readthedocs.io/en/latest/faq.html#buffer-donation."
    if platform not in _platforms_with_donation:
      msg = f"Donation is not implemented for {platform}.\n{msg}"
    warnings.warn(f"Some donated buffers were not usable: {', '.join(unused_donations)}.\n{msg}")

  # HLO channels need to start at 1
  channel_iter = itertools.count(1)
  # Create a keepalives list that will be mutated during the lowering.
  keepalives: list[Any] = []
  host_callbacks: list[Any] = []

  dim_vars: Sequence[str]
  if not config.jax_dynamic_shapes:
    # Find the dimension variables
    all_dim_poly = [d for aval in jaxpr.in_avals if hasattr(aval, "shape")
                    for d in aval.shape if not core.is_constant_dim(d)]
    dim_vars = tuple(sorted(functools.reduce(lambda acc, new: acc.union(new.get_vars()),
                                             all_dim_poly, set())))
  else:
    dim_vars = ()

  arg_op_shardings = (
      map(_to_logical_op_sharding, jaxpr.in_avals, arg_shardings)
      if arg_shardings is not None else arg_shardings)
  result_op_shardings = (
      map(_to_logical_op_sharding, jaxpr.out_avals, result_shardings)
      if result_shardings is not None else result_shardings)

  ctx = ModuleContext(backend_or_name, platform, axis_context, name_stack,
                      keepalives, channel_iter, host_callbacks,
                      override_lowering_rules=override_lowering_rules,
                      shape_poly_state=ShapePolyLoweringState(dim_vars))
  with ctx.context, ir.Location.unknown(ctx.context):
    # Remove module name characters that XLA would alter. This ensures that
    # XLA computation preserves the module name.
    attrs = ctx.module.operation.attributes
    module_name = _module_name_regex.sub("_", module_name)
    attrs["sym_name"] = ir.StringAttr.get(module_name)
    attrs["mhlo.num_replicas"] = i32_attr(num_replicas)
    attrs["mhlo.num_partitions"] = i32_attr(num_partitions)
    lower_jaxpr_to_fun(
        ctx, "main", jaxpr, ordered_effects, public=True, create_tokens=True,
        replace_tokens_with_dummy=True,
        num_output_tokens=0,
        replicated_args=replicated_args,
        arg_shardings=arg_op_shardings,
        result_shardings=result_op_shardings,
        input_output_aliases=input_output_aliases,
        arg_names=arg_names,
        result_names=result_names)

  try:
    if not ctx.module.operation.verify():
      module_string = module_to_string(ctx.module)
      raise ValueError(
          f"Cannot lower jaxpr with verifier errors: {module_string}")
  except ir.MLIRError as e:
    module_string = module_to_string(ctx.module)
    raise ValueError(
        f"Cannot lower jaxpr with verifier errors: {module_string}") from e

  return LoweringResult(ctx.module, ctx.keepalives, ctx.host_callbacks,
                        ctx.shape_poly_state)
