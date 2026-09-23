def _cpp_pmap(
    fun: Callable,
    axis_name: AxisName | None = None,
    *,
    in_axes=0,
    out_axes=0,
    static_broadcasted_argnums: int | Iterable[int] = (),
    devices: Sequence[xc.Device] | None = None,  # noqa: F811
    backend: str | None = None,
    axis_size: int | None = None,
    donate_argnums: int | Iterable[int] = (),
  ) -> Any:
  axis_name, static_broadcasted_tuple, donate_tuple = _shared_code_pmap(
      fun, axis_name, static_broadcasted_argnums, donate_argnums, in_axes,
      out_axes)
  del static_broadcasted_argnums, donate_argnums

  @api_boundary
  def cache_miss(*args, **kwargs):
    p = _prepare_pmap(fun, in_axes, out_axes, static_broadcasted_tuple,
                      donate_tuple, devices, backend,
                      axis_size, args, kwargs)
    for arg in p.flat_args:
      dispatch.check_arg(arg)

    params = dict(
        backend=backend,
        axis_name=axis_name,
        axis_size=p.local_axis_size,
        global_axis_size=p.global_axis_size,
        devices=p.devices,
        in_axes=p.in_axes_flat,
        out_axes_thunk=p.out_axes_thunk,
        name=p.flat_fun.__name__,
        donated_invars=p.donated_invars,
        is_explicit_global_axis_size=p.is_explicit_global_axis_size,
    )

    map_bind_continuation, top_trace, fun_, tracers, params = (
        core.map_bind_with_continuation(pxla.xla_pmap_p, p.flat_fun,
                                        *p.flat_args, **params))
    execute: Callable | None = None
    if isinstance(top_trace, core.EvalTrace):
      execute = pxla.xla_pmap_impl_lazy(fun_, *tracers, **params)
      out = map_bind_continuation(execute(*tracers))
    else:
      out = map_bind_continuation(
          pxla.xla_pmap_p.process(top_trace, fun_, tracers, params))

    out_tree, out_flat = p.out_tree, out
    out_pytree_def = out_tree()
    out = tree_unflatten(out_pytree_def, out_flat)

    ### Decide whether we can support the C++ fast path
    use_fastpath = False
    if execute is not None and isinstance(execute, pxla.ExecuteReplicated):
      execute_replicated = typing.cast(pxla.ExecuteReplicated, execute)
      use_fastpath = (
        # TODO(sharadmv): Enable effects in replicated computation
        not execute_replicated.has_unordered_effects
        and not execute_replicated.has_host_callbacks and
        # No tracers in the outputs.
        all(isinstance(x, xc.ArrayImpl) for x in out_flat))

    ### If we can use the fastpath, we return required info to the caller.
    if use_fastpath:
      execute_replicated = typing.cast(pxla.ExecuteReplicated, execute)
      out_handler = execute_replicated.out_handler
      in_handler = execute_replicated.in_handler

      out_array_shardings = [out.sharding for out in out_flat]
      out_committed = [out._committed for out in out_flat]
      input_sharding_specs = None
      out_sharding_specs = None
      out_indices = None
      # TODO(phawkins): remove sharding specs once minimum jaxlib is 0.4.15.
      if xla_extension_version < 176:
        input_sharding_specs = [
            i.sharding_spec for i in in_handler.in_shardings
        ]
        out_sharding_specs = [
            s.sharding_spec for s in out_handler.out_shardings
        ]
        out_indices = [
            tuple(s.devices_indices_map(a.shape).values())
            for s, a in safe_zip(
                out_handler.out_shardings, out_handler.out_avals
            )
        ]

      fastpath_data = _PmapFastpathData(
          version=1,
          xla_executable=execute_replicated.xla_executable,
          in_handler=in_handler,
          out_handler=out_handler,
          out_pytree_def=out_pytree_def,
          input_sharding_specs=input_sharding_specs,
          input_devices=in_handler.local_devices,
          input_indices=in_handler.input_indices,
          input_array_shardings=in_handler.in_shardings,
          out_sharding_specs=out_sharding_specs,
          out_indices=out_indices,
          out_avals=out_handler.out_avals,
          out_array_shardings=out_array_shardings,
          out_committed=out_committed,
      )

    else:
      fastpath_data = None

    return out, fastpath_data

  cpp_mapped_f = pmap_lib.pmap(
      fun, cache_miss, static_broadcasted_tuple, pxla.shard_arg,
      pytree_registry=tree_util.default_registry)
  _pmap_cache_clears.add(cpp_mapped_f)

  pmap_f = wraps(fun)(cpp_mapped_f)

  pmap_f.lower = _pmap_lower(
      fun, axis_name, in_axes, out_axes, static_broadcasted_tuple, devices,
      backend, axis_size, donate_tuple)

  return pmap_f
