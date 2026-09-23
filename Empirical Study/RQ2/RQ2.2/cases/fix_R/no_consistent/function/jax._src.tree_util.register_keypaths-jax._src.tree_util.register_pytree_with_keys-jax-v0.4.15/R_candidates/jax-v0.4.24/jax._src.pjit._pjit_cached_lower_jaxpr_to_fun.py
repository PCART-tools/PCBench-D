def _pjit_cached_lower_jaxpr_to_fun(ctx, name, jaxpr, effects, in_shardings,
                                    out_shardings, api_name):
  mod_ctx = ctx.module_context
  axis_ctx = ctx.module_context.axis_context
  num_devices = None
  if isinstance(axis_ctx, sharding_impls.ShardingContext):
    num_devices = axis_ctx.num_devices
  elif isinstance(axis_ctx, sharding_impls.SPMDAxisContext):
    num_devices = axis_ctx.mesh.size
  key = (pjit_p, name, jaxpr, effects, num_devices,
         pxla.SemanticallyEqualShardings(in_shardings),
         pxla.SemanticallyEqualShardings(out_shardings), api_name)

  func = mod_ctx.cached_primitive_lowerings.get(key, None)
  if func is None:
    arg_shardings = [None if is_unspecified(i) else i._to_xla_hlo_sharding(aval.ndim)
                     for aval, i in zip(ctx.avals_in, in_shardings)]
    result_shardings = [None if is_unspecified(o) else o._to_xla_hlo_sharding(aval.ndim)
                        for aval, o in zip(ctx.avals_out, out_shardings)]
    # TODO(b/228598865): inlined calls cannot have shardings set directly on the
    # inputs or outputs because they are lost during MLIR->HLO conversion.
    # using_sharding_annotation=False means we add an identity operation instead.
    func = mlir.lower_jaxpr_to_fun(
        mod_ctx, name, jaxpr, effects, arg_shardings=arg_shardings,
        result_shardings=result_shardings, use_sharding_annotations=False,
        api_name=api_name)
    mod_ctx.cached_primitive_lowerings[key] = func
  return func
