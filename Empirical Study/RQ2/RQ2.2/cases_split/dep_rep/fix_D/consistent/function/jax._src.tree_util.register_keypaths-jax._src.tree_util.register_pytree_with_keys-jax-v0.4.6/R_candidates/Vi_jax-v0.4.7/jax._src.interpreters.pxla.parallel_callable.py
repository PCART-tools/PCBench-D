@lu.cache
def parallel_callable(fun: lu.WrappedFun,
                      backend_name: Optional[str],
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
                      *avals):
  pmap_computation = lower_parallel_callable(
      fun, backend_name, axis_name, axis_size, global_axis_size, devices, name,
      in_axes, out_axes_thunk, donated_invars, global_arg_shapes,
      is_explicit_global_axis_size, avals, lowering_platform=None)
  pmap_executable = pmap_computation.compile()
  return WeakRefList([pmap_executable.unsafe_call, pmap_executable.fingerprint])
