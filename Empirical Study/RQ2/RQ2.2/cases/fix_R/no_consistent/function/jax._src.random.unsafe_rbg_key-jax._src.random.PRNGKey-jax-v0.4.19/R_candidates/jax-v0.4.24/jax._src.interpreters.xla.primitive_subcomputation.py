def primitive_subcomputation(platform: str, axis_env: AxisEnv,
                             prim: core.Primitive,
                             avals_in: Sequence[core.AbstractValue],
                             avals_out: Sequence[core.AbstractValue],
                             **params):
  c = xc.XlaBuilder(f"primitive_computation_{prim.name}")
  counts = it.count()
  xla_args = [parameter(c, next(counts), xla_shape)
              for a in avals_in for xla_shape in aval_to_xla_shapes(a)]
  if (platform is not None and
      prim in _backend_specific_translations[platform]):
    rule = _backend_specific_translations[platform][prim]
  elif prim in _translations:
    rule = _translations[prim]

  ctx = TranslationContext(builder=c, platform=platform, axis_env=axis_env,
                           name_stack=source_info_util.new_name_stack())
  ans = rule(ctx, avals_in, avals_out, *xla_args, **params)

  if prim.multiple_results:
    return c.build(xops.Tuple(c, ans))
  else:
    x, = ans
    return c.build(x)
