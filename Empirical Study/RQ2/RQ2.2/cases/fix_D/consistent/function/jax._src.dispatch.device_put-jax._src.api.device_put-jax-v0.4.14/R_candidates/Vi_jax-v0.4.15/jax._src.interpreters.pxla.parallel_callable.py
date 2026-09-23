@lu.cache
def parallel_callable(fun: lu.WrappedFun,
                      backend_name: str | None,
                      axis_name: core.AxisName,
                      axis_size: int,
                      global_axis_size: int,
                      devices: Sequence[Any] | None,
                      name: str,
                      in_axes: Sequence[int | None],
                      out_axes_thunk: Callable[[], Sequence[int | None]],
                      donated_invars: Sequence[bool],
                      is_explicit_global_axis_size: bool,
                      *avals):
  pmap_computation = lower_parallel_callable(
      fun, backend_name, axis_name, axis_size, global_axis_size, devices, name,
      in_axes, out_axes_thunk, donated_invars,
      is_explicit_global_axis_size, avals, lowering_platform=None)
  pmap_executable = pmap_computation.compile()
  return WeakRefList([pmap_executable.unsafe_call, pmap_executable.fingerprint])
