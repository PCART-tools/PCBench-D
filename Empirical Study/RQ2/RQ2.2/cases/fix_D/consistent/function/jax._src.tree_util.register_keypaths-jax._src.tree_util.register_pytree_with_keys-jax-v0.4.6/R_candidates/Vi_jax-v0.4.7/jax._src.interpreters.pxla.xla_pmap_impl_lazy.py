def xla_pmap_impl_lazy(
    fun: lu.WrappedFun,
    *args,
    backend: Optional[str],
    axis_name: core.AxisName,
    axis_size: int,
    global_axis_size: int,
    devices: Optional[Sequence[Any]],
    name: str,
    in_axes: Sequence[Optional[int]],
    out_axes_thunk: Callable[[], Sequence[Optional[int]]],
    donated_invars: Sequence[bool],
    global_arg_shapes: Sequence[Optional[Tuple[int, ...]]],
    is_explicit_global_axis_size: bool,
) -> Callable:
  if (config.jax_disable_jit and config.jax_eager_pmap and
      not is_explicit_global_axis_size and not any(d for d in donated_invars)
      and not all(g is not None for g in global_arg_shapes)):
    def _emap_apply_fn(*args):
      return _emap_impl(fun, *args, backend=backend, axis_name=axis_name,
                        axis_size=axis_size, global_axis_size=global_axis_size,
                        devices=devices, name=name, in_axes=in_axes,
                        out_axes_thunk=out_axes_thunk,
                        donated_invars=donated_invars,
                        global_arg_shapes=global_arg_shapes,
                        is_explicit_global_axis_size=is_explicit_global_axis_size)
    return _emap_apply_fn
  abstract_args = unsafe_map(xla.abstractify, args)
  compiled_fun, fingerprint = parallel_callable(
      fun, backend, axis_name, axis_size, global_axis_size, devices, name,
      in_axes, out_axes_thunk, donated_invars, global_arg_shapes,
      is_explicit_global_axis_size, *abstract_args)

  # Don't re-abstractify args unless logging is enabled for performance.
  if config.jax_distributed_debug:
    distributed_debug_log(("Running pmapped function", name),
                          ("python function", fun.f),
                          ("devices", devices),
                          ("abstract args", map(xla.abstractify, args)),
                          ("fingerprint", fingerprint))
  return compiled_fun
