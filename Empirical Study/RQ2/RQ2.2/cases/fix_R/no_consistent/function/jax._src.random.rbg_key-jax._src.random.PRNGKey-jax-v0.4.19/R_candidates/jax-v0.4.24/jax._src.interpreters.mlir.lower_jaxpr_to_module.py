def lower_jaxpr_to_module(
    module_name: str,
    jaxpr: core.ClosedJaxpr,
    *,
    ordered_effects: list[core.Effect],
    backend_or_name: str | xb.XlaBackend | None,
    platforms: Sequence[str],
    axis_context: AxisContext,
    name_stack: source_info_util.NameStack,
    donated_args: Sequence[bool],
    replicated_args: Sequence[bool] | None = None,
    arg_shardings: Sequence[XLACompatibleSharding | None] | None = None,
    result_shardings: Sequence[XLACompatibleSharding | None] | None = None,
    in_layouts: Sequence[XLACompatibleLayout | None | LayoutRequest] | None = None,
    out_layouts: Sequence[XLACompatibleLayout | None | LayoutRequest] | None = None,
    arg_names: Sequence[str | None] | None = None,
    result_names: Sequence[str | None] | None = None,
    num_replicas: int = 1,
    num_partitions: int = 1,
    all_default_mem_kind: bool = True,
    lowering_parameters: LoweringParameters,
) -> LoweringResult:
  """Lowers a top-level jaxpr to an MLIR module.

  Handles the quirks of the argument/return value passing conventions of the
  runtime.
  """
  platforms = tuple(map(xb.canonicalize_platform, platforms))

  input_output_aliases = None
  in_avals = (jaxpr.in_avals if arg_shardings is None else
              map(sharded_aval, jaxpr.in_avals, arg_shardings))
  out_avals = (jaxpr.out_avals if result_shardings is None else
               map(sharded_aval, jaxpr.out_avals, result_shardings))
  if all_default_mem_kind:
    arg_memory_kinds = None
    result_memory_kinds = None
  else:
    arg_memory_kinds = (map(_get_mem_kind, arg_shardings)
                        if arg_shardings is not None else None)
    result_memory_kinds = (map(_get_mem_kind, result_shardings)
                          if result_shardings is not None else None)

  xla_donated_args = None
  platforms_with_donation = [p for p in platforms
                             if p in _platforms_with_donation]
  if platforms_with_donation:
    if len(platforms_with_donation) != len(platforms):
      raise NotImplementedError(
        "In multi-platform lowering either all or no lowering platforms "
        f"should support donation. Lowering for {platforms} of which "
        f"only {platforms_with_donation} support donation")
    if num_partitions > 1 and xla_extension_version >= 220 and (
        result_shardings is None or all(s is None for s in result_shardings)):
      xla_donated_args = donated_args
    if xla_donated_args is None:
      input_output_aliases, donated_args = _set_up_aliases(
        in_avals, out_avals, donated_args, arg_memory_kinds,
        result_memory_kinds)
  unlowerable_effects = lowerable_effects.filter_not_in(jaxpr.effects)
  if unlowerable_effects:
    raise ValueError(f'Cannot lower jaxpr with effects: {jaxpr.effects}')
  if xla_donated_args is None and any(donated_args):
    unused_donations = [str(a) for a, d in zip(in_avals, donated_args) if d]
    msg = "See an explanation at https://jax.readthedocs.io/en/latest/faq.html#buffer-donation."
    if not platforms_with_donation:
      msg = f"Donation is not implemented for {platforms}.\n{msg}"
    if unused_donations:
      warnings.warn("Some donated buffers were not usable:"
                    f" {', '.join(unused_donations)}.\n{msg}")

  if xla_donated_args is not None:
    assert input_output_aliases is None
  if input_output_aliases is not None:
    assert xla_donated_args is None

  # Delete donated_args by default here, since it's not needed beyond this point
  del donated_args

  # HLO channels need to start at 1
  channel_iter = itertools.count(1)
  # Create a keepalives list that will be mutated during the lowering.
  keepalives: list[Any] = []
  host_callbacks: list[Any] = []

  dim_vars: Sequence[str]
  if not config.dynamic_shapes.value:
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

  arg_layouts = (map(_to_xla_layout, in_layouts) if in_layouts is not None
                  else in_layouts)
  result_layouts = (map(_to_xla_layout, out_layouts) if out_layouts is not None
                    else out_layouts)

  ctx = ModuleContext(backend_or_name=backend_or_name,
                      platforms=platforms, axis_context=axis_context,
                      name_stack=name_stack,
                      keepalives=keepalives,
                      channel_iterator=channel_iter,
                      host_callbacks=host_callbacks,
                      lowering_parameters=lowering_parameters,
                      shape_poly_state=ShapePolyLoweringState(
                          dim_vars, lowering_parameters.platforms))
  with ctx.context, ir.Location.unknown(ctx.context):
    # Remove module name characters that XLA would alter. This ensures that
    # XLA computation preserves the module name.
    attrs = ctx.module.operation.attributes
    module_name = _module_name_regex.sub("_", module_name)
    attrs["sym_name"] = ir.StringAttr.get(module_name)
    attrs["mhlo.num_replicas"] = i32_attr(num_replicas)
    attrs["mhlo.num_partitions"] = i32_attr(num_partitions)
    replace_tokens_with_dummy = lowering_parameters.replace_tokens_with_dummy
    lower_jaxpr_to_fun(
        ctx, "main", jaxpr, ordered_effects, public=True,
        create_tokens=replace_tokens_with_dummy,
        replace_tokens_with_dummy=replace_tokens_with_dummy,
        num_output_tokens=0,
        replicated_args=replicated_args,
        arg_shardings=arg_op_shardings,
        result_shardings=result_op_shardings,
        input_output_aliases=input_output_aliases,
        xla_donated_args=xla_donated_args,
        arg_names=arg_names,
        result_names=result_names,
        arg_memory_kinds=arg_memory_kinds,
        result_memory_kinds=result_memory_kinds,
        arg_layouts=arg_layouts,
        result_layouts=result_layouts)

  try:
    if not ctx.module.operation.verify():
      raise ValueError(
          "Cannot lower jaxpr with verifier errors." +
          dump_module_message(ctx.module, "verification"))
  except ir.MLIRError as e:
    msg_lines = ["Cannot lower jaxpr with verifier errors:"]
    def emit_diagnostic_info(d):
      msg_lines.append(f"\t{d.message}")
      msg_lines.append(f"\t\tat {d.location}")
      for n in d.notes:
        emit_diagnostic_info(n)
    for d in e.error_diagnostics:
      emit_diagnostic_info(d)
    raise ValueError("\n".join(msg_lines) +
                     dump_module_message(ctx.module, "verification")) from e

  return LoweringResult(ctx.module, ctx.keepalives, ctx.host_callbacks,
                        ctx.shape_poly_state)
