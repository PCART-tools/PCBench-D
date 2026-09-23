def _cpp_pmap(
    fun: Callable,
    axis_name: Optional[AxisName] = None,
    *,
    in_axes=0,
    out_axes=0,
    static_broadcasted_argnums: Union[int, Iterable[int]] = (),
    devices: Optional[Sequence[xc.Device]] = None,  # noqa: F811
    backend: Optional[str] = None,
    axis_size: Optional[int] = None,
    donate_argnums: Union[int, Iterable[int]] = (),
    global_arg_shapes: Optional[Tuple[Tuple[int, ...], ...]] = None,
  ) -> Any:
  axis_name, static_broadcasted_tuple, donate_tuple = _shared_code_pmap(
      fun, axis_name, static_broadcasted_argnums, donate_argnums, in_axes,
      out_axes)
  del static_broadcasted_argnums, donate_argnums

  @api_boundary
  def cache_miss(*args, **kwargs):
    f_pmapped_ = _get_f_mapped(
        fun=fun,
        axis_name=axis_name,
        in_axes=in_axes,
        out_axes=out_axes,
        static_broadcasted_tuple=static_broadcasted_tuple,
        devices=devices,
        backend=backend,
        axis_size=axis_size,
        global_arg_shapes=global_arg_shapes,
        donate_tuple=donate_tuple)

    out_tree, out_flat = f_pmapped_(*args, **kwargs)
    out_pytree_def = out_tree()
    out = tree_unflatten(out_pytree_def, out_flat)

    ### Decide whether we can support the C++ fast path
    execute: Optional[functools.partial] = None
    execute = pxla.parallel_callable.most_recent_entry()
    use_fastpath = (
        execute is not None and
        # We don't support JAX extension backends.
        isinstance(execute[0], pxla.ExecuteReplicated) and
        # TODO(sharadmv): Enable effects in replicated computation
        not execute[0].has_unordered_effects and
        # No tracers in the outputs. Checking for ShardedDeviceArray should be
        # sufficient, but we use the more general `DeviceArray`.
        all(isinstance(x, device_array.DeviceArray) for x in out_flat))
    ### If we can use the fastpath, we return required info to the caller.
    if use_fastpath:
      execute_replicated = execute[0]
      out_handler = execute_replicated.out_handler
      in_handler = execute_replicated.in_handler
      out_indices = [tuple(s.devices_indices_map(a.shape).values())
                     for s, a in safe_zip(out_handler.out_shardings, out_handler.out_avals)]
      fastpath_data = _PmapFastpathData(
          version=1,
          xla_executable=execute_replicated.xla_executable,
          in_handler=in_handler,
          out_handler=out_handler,
          out_pytree_def=out_pytree_def,
          input_sharding_specs=[i.sharding_spec for i in in_handler.in_shardings],
          input_devices=in_handler.local_devices,
          input_indices=in_handler.input_indices,
          out_sharding_specs=[s.sharding_spec for s in out_handler.out_shardings],
          out_indices=out_indices,
          out_avals=out_handler.out_avals,
      )

    else:
      fastpath_data = None

    return out, fastpath_data

  cpp_mapped_f = pmap_lib.pmap(fun, cache_miss,
                               static_broadcasted_tuple, pxla._shard_arg)

  pmap_f = wraps(fun)(cpp_mapped_f)

  pmap_f.lower = _pmap_lower(
      fun, axis_name, in_axes, out_axes, static_broadcasted_tuple, devices,
      backend, axis_size, global_arg_shapes, donate_tuple)

  return pmap_f
