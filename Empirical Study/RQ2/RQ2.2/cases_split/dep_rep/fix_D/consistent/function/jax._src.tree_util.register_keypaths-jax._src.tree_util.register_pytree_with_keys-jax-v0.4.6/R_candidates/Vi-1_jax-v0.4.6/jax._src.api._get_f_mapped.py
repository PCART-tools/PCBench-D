def _get_f_mapped(
    *,
    fun: Callable,
    axis_name: Optional[AxisName],
    in_axes=0,
    out_axes=0,
    static_broadcasted_tuple: Tuple[int, ...],
    devices: Optional[Sequence[xc.Device]],  # noqa: F811
    backend: Optional[str],
    axis_size: Optional[int],
    donate_tuple: Tuple[int, ...],
    global_arg_shapes: Optional[Tuple[Tuple[int, ...], ...]],
  ):
  def pmap_f(*args, **kwargs):
    p = _prepare_pmap(
        fun, in_axes, out_axes, static_broadcasted_tuple, donate_tuple,
        global_arg_shapes, devices, backend, axis_size, args, kwargs)
    for arg in p.flat_args:
      dispatch.check_arg(arg)
    out = pxla.xla_pmap(
        p.flat_fun, *p.flat_args, backend=backend, axis_name=axis_name,
        axis_size=p.local_axis_size, global_axis_size=p.global_axis_size,
        devices=p.devices,
        in_axes=p.in_axes_flat, out_axes_thunk=p.out_axes_thunk,
        name=p.flat_fun.__name__, donated_invars=p.donated_invars,
        global_arg_shapes=p.global_arg_shapes_flat,
        is_explicit_global_axis_size=p.is_explicit_global_axis_size)
    return p.out_tree, out

  return pmap_f
