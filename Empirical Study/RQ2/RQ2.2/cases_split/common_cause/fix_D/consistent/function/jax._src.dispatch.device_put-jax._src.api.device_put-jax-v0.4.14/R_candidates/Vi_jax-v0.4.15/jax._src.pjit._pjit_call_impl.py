def _pjit_call_impl(*args, jaxpr,
                    in_shardings, out_shardings, resource_env,
                    donated_invars, name, keep_unused, inline):
  def call_impl_cache_miss(*args_, **kwargs_):
    out_flat, compiled = _pjit_call_impl_python(
        *args, jaxpr=jaxpr, in_shardings=in_shardings,
        out_shardings=out_shardings, resource_env=resource_env,
        donated_invars=donated_invars, name=name, keep_unused=keep_unused,
        inline=inline)
    fastpath_data = _get_fastpath_data(
        compiled, tree_structure(out_flat), args, out_flat)
    return out_flat, fastpath_data

  f = _get_jaxpr_as_fun(
      jaxpr, tuple(getattr(i, '_original_sharding', i) for i in in_shardings),
      tuple(getattr(o, '_original_sharding', o) for o in out_shardings),
      resource_env, donated_invars, name, keep_unused, inline)
  donated_argnums = [i for i, d in enumerate(donated_invars) if d]
  has_explicit_sharding = _pjit_explicit_sharding(
      in_shardings, out_shardings, None, None)
  return xc._xla.pjit(name, f, call_impl_cache_miss, [], [], donated_argnums,
                      tree_util.default_registry,
                      _get_cpp_global_cache(has_explicit_sharding))(*args)
