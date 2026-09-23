def _emap_impl(fun: lu.WrappedFun, *args,
               backend: str | None,
               axis_name: core.AxisName,
               axis_size: int,
               global_axis_size: int,
               devices: Sequence[Any] | None,
               name: str,
               in_axes: Sequence[int | None],
               out_axes_thunk: Callable[[], Sequence[int | None]],
               donated_invars: Sequence[bool],
               is_explicit_global_axis_size: bool,
               ):
  from jax._src import array
  # TODO(sharadmv,mattjj): implement these cases
  if any(d for d in donated_invars):
    raise NotImplementedError("Buffer donation not supported in eager pmap.")
  if is_explicit_global_axis_size:
    raise NotImplementedError("Non-default global_axis_size not supported in "
                              "eager pmap.")

  emap_info = EmapInfo(backend, devices)
  shard_axes = [{} if in_axis is None else {axis_name: in_axis} for in_axis in in_axes]
  with core.new_base_main(MapTrace, emap_info=emap_info) as main:
    with core.new_sublevel(), core.extend_axis_env(axis_name, axis_size, main):
      t = main.with_cur_sublevel()
      tracers = [
          MapTracer(t, arg, s) for arg, s in zip(args, shard_axes)]
      ans = fun.call_wrapped(*tracers)
      out_tracers = map(t.full_raise, ans)
      outvals, out_axes_src = unzip2((t.val, t.shard_axes) for t in out_tracers)
    del main
  out_axes = out_axes_thunk()

  platform = xb.get_backend(backend).platform
  donate_argnums = (1,) if platform in {"cuda", "rocm", "tpu"} else ()
  new_outvals = []
  for out_axis_src, out_axis, outval in zip(out_axes_src, out_axes, outvals):
    with jax.disable_jit(False):
      donate_argnums_ = donate_argnums
      if isinstance(outval, array.ArrayImpl):
        # We don't want to donate if it's already sharded.
        donate_argnums_ = ()
      out = jax.pmap(
          lambda _, x: x,
          in_axes=(0, out_axis_src.get(axis_name)),
          out_axes=out_axis,
          devices=(None if devices is None else list(devices)),
          backend=backend,
          donate_argnums=donate_argnums_)(np.arange(axis_size), outval)
      new_outvals.append(out)
  return new_outvals
