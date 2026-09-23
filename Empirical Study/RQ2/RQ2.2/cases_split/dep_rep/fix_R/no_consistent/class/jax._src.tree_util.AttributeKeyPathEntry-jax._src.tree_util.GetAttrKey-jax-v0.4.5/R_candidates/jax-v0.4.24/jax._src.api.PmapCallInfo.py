class PmapCallInfo(NamedTuple):
  flat_fun: lu.WrappedFun
  in_tree: PyTreeDef
  out_tree: Callable[[], PyTreeDef]
  flat_args: Sequence[Any]
  donated_invars: Sequence[bool]
  in_axes_flat: Sequence[int | None]
  local_axis_size: int
  out_axes_thunk: Callable
  devices: Sequence[xc.Device] | None
  global_axis_size: int
  is_explicit_global_axis_size: bool
