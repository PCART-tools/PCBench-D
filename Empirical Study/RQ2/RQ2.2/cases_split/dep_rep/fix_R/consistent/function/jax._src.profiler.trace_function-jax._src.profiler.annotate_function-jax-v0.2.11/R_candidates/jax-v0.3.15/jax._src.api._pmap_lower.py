def _pmap_lower(fun, axis_name, in_axes, out_axes, static_broadcasted_tuple,
                devices, backend, axis_size, global_arg_shapes, donate_tuple):  # noqa: F811
  """Make a ``lower`` method for pmapped functions."""
  # If the function we returned from ``pmap`` were a class instance,
  # this might naturally be a method, with ``fun`` as a ``self`` and
  # all the other arguments stored as attributes.
  @api_boundary
  def lower(*args, **kwargs) -> stages.Lowered:
    """Lower a parallel-mapped form of this function for the given arguments.

    A parallel-mapped and lowered function is staged out of Python and
    translated to a compiler's input language, possibly in a
    backend-dependent manner. It is ready for compilation but is not yet
    compiled. It represents a function intended for SPMD execution on
    multiple devices.

    Returns:
      A ``Lowered`` instance representing the post-map lowering.
    """
    p = _prepare_pmap(
        fun, in_axes, out_axes, static_broadcasted_tuple, donate_tuple,
        global_arg_shapes, devices, args, kwargs)
    abstract_args = list(map(xla.abstractify, p.flat_args))
    computation = pxla.lower_parallel_callable(
        p.flat_fun, backend, axis_name,
        axis_size=p.local_axis_size, global_axis_size=axis_size,
        devices=p.devices,
        name=p.flat_fun.__name__,
        in_axes=p.in_axes_flat,
        out_axes_thunk=p.out_axes_thunk,
        donated_invars=p.donated_invars,
        global_arg_shapes=p.global_arg_shapes_flat,
        avals=abstract_args)
    return stages.Lowered.from_flat_info(
        computation, p.in_tree, abstract_args, donate_tuple, p.out_tree())

  return lower
