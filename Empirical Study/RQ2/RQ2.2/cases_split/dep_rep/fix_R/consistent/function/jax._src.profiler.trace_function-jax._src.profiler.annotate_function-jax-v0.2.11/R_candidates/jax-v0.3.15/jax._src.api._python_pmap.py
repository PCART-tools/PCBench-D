def _python_pmap(
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
  ) -> stages.Wrapped:
  """The Python only implementation."""
  axis_name, static_broadcasted_tuple, donate_tuple = _shared_code_pmap(
      fun, axis_name, static_broadcasted_argnums, donate_argnums, in_axes,
      out_axes)

  @wraps(fun)
  @api_boundary
  def pmap_f(*args, **kwargs):
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
    return tree_unflatten(out_tree(), out_flat)

  pmap_f.lower = _pmap_lower(
      fun, axis_name, in_axes, out_axes, static_broadcasted_tuple, devices,
      backend, axis_size, global_arg_shapes, donate_tuple)

  return pmap_f
