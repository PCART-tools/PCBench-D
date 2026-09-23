class PmapCallInfo(NamedTuple):
  flat_fun: lu.WrappedFun
  in_tree: PyTreeDef
  out_tree: PyTreeDef
  flat_args: Sequence[Any]
  donated_invars: Sequence[bool]
  in_axes_flat: Sequence[Optional[int]]
  local_axis_size: int
  global_arg_shapes_flat: Sequence[Optional[Tuple[int, ...]]]
  out_axes_thunk: HashableFunction
  devices: Optional[Sequence[xc.Device]]
