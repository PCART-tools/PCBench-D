def jaxpr_subcomp(ctx: ModuleContext, jaxpr: core.Jaxpr,
                  tokens: TokenSet,
                  consts: Sequence[Sequence[ir.Value]],
                  *args: Sequence[ir.Value],
                  dim_var_values: Sequence[ir.Value]
                  ) -> tuple[Sequence[Sequence[ir.Value]], TokenSet]:
  """Lowers a jaxpr into MLIR, inlined into an existing function.

  Assumes that an MLIR context, location, and insertion point are set.

  dim_var_values: the list of dimension variables values in the current
    IR function, in the order of ctx.shape_poly_state.dim_vars.
  """
  assert "gpu" not in ctx.platforms
  def read(v: core.Atom) -> Sequence[ir.Value]:
    if type(v) is core.Literal:
      return ir_constants(xla.canonicalize_dtype(v.val))
    else:
      assert isinstance(v, core.Var)
      return env[v]

  def aval(v: core.Atom) -> core.AbstractValue:
    if type(v) is core.Literal:
      return xla.abstractify(v.val)
    else:
      return v.aval

  def write(v: core.Var, node: Sequence[ir.Value]):
    assert node is not None
    env[v] = tuple(node)

  def get_override_lowering_rule(primitive: core.Primitive) -> LoweringRule | None:
    if ctx.lowering_parameters.override_lowering_rules is None:
      return None
    for p, rule in ctx.lowering_parameters.override_lowering_rules:
      if primitive is p:
        return rule
    return None

  env: dict[core.Var, tuple[ir.Value, ...]] = {}

  assert len(args) == len(jaxpr.invars), (jaxpr, args)
  assert len(consts) == len(jaxpr.constvars), (jaxpr, consts)
  assert all(isinstance(v, ir.Value) for vs in consts for v in vs), consts
  assert len(ctx.shape_poly_state.dim_vars) == len(dim_var_values), (ctx.shape_poly_state.dim_vars, dim_var_values)
  map(write, jaxpr.constvars, consts)
  map(write, jaxpr.invars, args)
  last_used = core.last_used(jaxpr)
  for eqn in jaxpr.eqns:
    in_nodes = map(read, eqn.invars)
    assert isinstance(ctx.name_stack, source_info_util.NameStack), type(ctx.name_stack)
    source_info = eqn.source_info.replace(
        name_stack=ctx.name_stack + eqn.source_info.name_stack)
    loc = _source_info_to_location(ctx, eqn.primitive, eqn.params, source_info)
    with source_info_util.user_context(eqn.source_info.traceback), loc:
      override_rule = get_override_lowering_rule(eqn.primitive)
      platform_rules: dict[str, LoweringRule] = {}
      default_rule: LoweringRule | None = None
      # See mlir.lower_per_platform for meaning of `platform_rules` and `default_rule`
      if override_rule is not None:
        default_rule = override_rule
      else:
        # First the platform-specific rules
        for p in ctx.platforms:
          if eqn.primitive in _platform_specific_lowerings[p]:
            platform_rules[p] = _platform_specific_lowerings[p][eqn.primitive]
          elif eqn.primitive in xla._backend_specific_translations[p]:
            platform_rules[p] = xla_fallback_lowering(eqn.primitive)
        # Now the default rule
        if eqn.primitive in _lowerings:
          default_rule = _lowerings[eqn.primitive]
        elif eqn.primitive in xla._translations:
          default_rule = xla_fallback_lowering(eqn.primitive)

      eqn_ctx = ctx.replace(name_stack=source_info.name_stack)
      effects = list(effects_lib.ordered_effects.filter_in(eqn.effects))
      tokens_in = tokens.subset(effects)
      avals_in = map(aval, eqn.invars)
      rule_ctx = LoweringRuleContext(
          module_context=eqn_ctx, primitive=eqn.primitive,
          avals_in=avals_in,
          avals_out=map(aval, eqn.outvars), tokens_in=tokens_in,
          tokens_out=None, dim_var_values=dim_var_values)
      if config.dynamic_shapes.value:
        axis_size_env = {d: read(d)[0]
                         for a in avals_in if type(a) is core.DShapedArray
                         for d in a.shape if type(d) is core.Var}
        rule_ctx = rule_ctx.replace(axis_size_env=axis_size_env)

      rule_inputs = map(_unwrap_singleton_ir_values, in_nodes)
      ans = lower_per_platform(rule_ctx, str(eqn.primitive),
                               platform_rules, default_rule,
                               eqn.effects,
                               *rule_inputs, **eqn.params)

      if effects:
        # If there were ordered effects in the primitive, there should be output
        # tokens we need for subsequent ordered effects.
        tokens_out = rule_ctx.tokens_out
        if tokens_out is None:
          raise ValueError(
              f'Lowering rule for `{eqn.primitive}` needs to set `tokens_out` '
              f'because it has effects: {eqn.effects}.')
        if tokens_out.effects() != tokens_in.effects():
          raise ValueError(
              f'Lowering rule for `{eqn.primitive}` '
              'returns incorrect set of output tokens. '
              f'Expected: {tuple(tokens_in.effects())} vs. Actual: {tuple(tokens_out.effects())}')
        tokens = tokens.update_tokens(tokens_out)

    try:
      out_nodes = tuple(map(wrap_singleton_ir_values, ans))
    except TypeError as e:
      raise ValueError("Output of translation rule must be iterable: "
                       f"{eqn}, got output {ans}") from e

    assert all(isinstance(v, tuple) for v in out_nodes), (ans, eqn)
    assert all(isinstance(v, ir.Value) for w in out_nodes for v in w), (
      ans, "lowering function returned a bad output", eqn)
    assert len(ans) == len(eqn.outvars), (ans, eqn)
    map(write, eqn.outvars, out_nodes)
    core.clean_up_dead_vars(eqn, env, last_used)
  return map(read, jaxpr.outvars), tokens
