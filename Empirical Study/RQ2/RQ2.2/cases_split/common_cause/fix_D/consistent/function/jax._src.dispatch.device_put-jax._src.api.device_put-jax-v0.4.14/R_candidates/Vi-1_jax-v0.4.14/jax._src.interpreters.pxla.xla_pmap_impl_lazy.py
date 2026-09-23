def xla_pmap_impl_lazy(
    fun: lu.WrappedFun,
    *args,
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
) -> Callable:
  if (config.jax_disable_jit and config.jax_eager_pmap and
      not is_explicit_global_axis_size and not any(d for d in donated_invars)):
    def _emap_apply_fn(*args):
      return _emap_impl(fun, *args, backend=backend, axis_name=axis_name,
                        axis_size=axis_size, global_axis_size=global_axis_size,
                        devices=devices, name=name, in_axes=in_axes,
                        out_axes_thunk=out_axes_thunk,
                        donated_invars=donated_invars,
                        is_explicit_global_axis_size=is_explicit_global_axis_size)
    return _emap_apply_fn
  abstract_args = unsafe_map(xla.abstractify, args)
  compiled_fun, fingerprint = parallel_callable(
      fun, backend, axis_name, axis_size, global_axis_size, devices, name,
      in_axes, out_axes_thunk, donated_invars,
      is_explicit_global_axis_size, *abstract_args)

  # Don't re-abstractify args unless logging is enabled for performance.
  if config.jax_distributed_debug:
    distributed_debug_log(("Running pmapped function", name),
                          ("python function", fun.f),
                          ("devices", devices),
                          ("abstract args", map(xla.abstractify, args)),
                          ("fingerprint", fingerprint))
  return compiled_fun
