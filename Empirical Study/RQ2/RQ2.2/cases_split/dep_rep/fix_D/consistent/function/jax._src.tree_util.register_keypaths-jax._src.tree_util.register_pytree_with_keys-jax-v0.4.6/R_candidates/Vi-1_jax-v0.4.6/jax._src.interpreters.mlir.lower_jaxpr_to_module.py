def lower_jaxpr_to_module(
    module_name: str,
    jaxpr: core.ClosedJaxpr,
    unordered_effects: List[core.Effect],
    ordered_effects: List[core.Effect],
    backend_or_name: Optional[Union[str, xb.XlaBackend]],
    platform: str,
    axis_context: AxisContext,
    name_stack: source_info_util.NameStack,
    donated_args: Sequence[bool],
    replicated_args: Optional[Sequence[bool]] = None,
    arg_shardings: Optional[Sequence[Optional[xc.OpSharding]]] = None,
    result_shardings: Optional[Sequence[Optional[xc.OpSharding]]] = None,
    arg_names: Optional[Sequence[str]] = None,
    result_names: Optional[Sequence[str]] = None,
) -> LoweringResult:
  """Lowers a top-level jaxpr to an MLIR module.

  Handles the quirks of the argument/return value passing conventions of the
  runtime.
  """
  platform = xb.canonicalize_platform(platform)
  if not xb.is_known_platform(platform):
    raise ValueError(f"Unknown platform {platform}")
  input_output_aliases = None
  in_avals = jaxpr.in_avals
  if arg_shardings is not None:
    in_avals = [
        sharded_aval(in_aval, in_sharding)
        for in_aval, in_sharding in zip(in_avals, arg_shardings)
    ]
  out_avals = jaxpr.out_avals
  if result_shardings is not None:
    out_avals = []
    for out_aval, out_sharding in zip(jaxpr.out_avals, result_shardings):
      if (out_aval is not core.abstract_token and
          core.is_opaque_dtype(out_aval.dtype)):
        # TODO(frostig,mattjj,necula): asserts a single physical aval
        out_aval, = out_aval.dtype._rules.physical_avals(out_aval)
      out_avals.append(sharded_aval(out_aval, out_sharding))

  if platform in _platforms_with_donation:
    input_output_aliases, donated_args = _set_up_aliases(
        in_avals, out_avals, donated_args)
  unlowerable_effects = lowerable_effects.filter_not_in(jaxpr.effects)
  if unlowerable_effects:
    raise ValueError(f'Cannot lower jaxpr with effects: {jaxpr.effects}')
  if any(donated_args):
    # TODO(tomhennigan): At call time we should mark these buffers as deleted.
    unused_donations = [str(a) for a, d in zip(in_avals, donated_args)
                        if d]
    msg = "See an explanation at https://jax.readthedocs.io/en/latest/faq.html#buffer-donation."
    if platform not in _platforms_with_donation:
      msg = f"Donation is not implemented for {platform}.\n{msg}"
    warnings.warn(f"Some donated buffers were not usable: {', '.join(unused_donations)}.\n{msg}")

  # HLO channels need to start at 1
  channel_iter = itertools.count(1)
  # Create a keepalives list that will be mutated during the lowering.
  keepalives: List[Any] = []
  host_callbacks: List[Any] = []

  dim_vars: Sequence[str]
  if not config.jax_dynamic_shapes:
    # Find the dimension variables
    all_dim_poly = [d
                    for aval in jaxpr.in_avals if hasattr(aval, "shape")
                    for d in aval.shape if not core.is_constant_dim(d)]
    dim_vars = tuple(sorted(functools.reduce(lambda acc, new: acc.union(new.get_vars()),
                                             all_dim_poly, set())))
  else:
    dim_vars = ()

  ctx = ModuleContext(backend_or_name, platform, axis_context, name_stack,
                      keepalives, channel_iter, host_callbacks, dim_vars=dim_vars)
  with ctx.context, ir.Location.unknown(ctx.context):
    # Remove module name characters that XLA would alter. This ensures that
    # XLA computation preserves the module name.
    module_name = _module_name_regex.sub("_", module_name)
    ctx.module.operation.attributes["sym_name"] = ir.StringAttr.get(
        module_name)
    unlowerable_effects = lowerable_effects.filter_not_in(jaxpr.effects)
    if unlowerable_effects:
      raise ValueError(
          f'Cannot lower jaxpr with unlowerable effects: {unlowerable_effects}')
    lower_jaxpr_to_fun(
        ctx, "main", jaxpr, ordered_effects, public=True, create_tokens=True,
        replace_tokens_with_dummy=True,
        num_output_tokens=0,
        replicated_args=replicated_args,
        arg_shardings=arg_shardings, result_shardings=result_shardings,
        input_output_aliases=input_output_aliases,
        arg_names=arg_names, result_names=result_names)

  if not ctx.module.operation.verify():
    module_string = module_to_string(ctx.module)
    raise ValueError(
        f"Cannot lower jaxpr with verifier errors: {module_string}")

  return LoweringResult(ctx.module, ctx.keepalives, ctx.host_callbacks)
