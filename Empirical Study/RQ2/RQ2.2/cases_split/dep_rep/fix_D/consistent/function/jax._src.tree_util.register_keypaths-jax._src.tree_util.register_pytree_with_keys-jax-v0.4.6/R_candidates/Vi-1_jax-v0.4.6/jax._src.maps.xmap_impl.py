def xmap_impl(fun: lu.WrappedFun, *args, name, in_axes, out_axes_thunk, donated_invars,
              global_axis_sizes, axis_resources, resource_env, backend,
              spmd_in_axes, spmd_out_axes_thunk, in_positional_semantics,
              out_positional_semantics):
  in_avals = [core.raise_to_shaped(core.get_aval(arg)) for arg in args]
  xmap_callable = make_xmap_callable(
      fun, name, in_axes, out_axes_thunk, donated_invars, global_axis_sizes,
      axis_resources, resource_env, backend,
      spmd_in_axes, spmd_out_axes_thunk, in_positional_semantics, out_positional_semantics,
      None, *in_avals).compile().unsafe_call
  distributed_debug_log(("Running xmapped function", name),
                        ("python function", fun.f),
                        ("mesh", resource_env.physical_mesh),
                        ("abstract args", in_avals))
  return xmap_callable(*args)
