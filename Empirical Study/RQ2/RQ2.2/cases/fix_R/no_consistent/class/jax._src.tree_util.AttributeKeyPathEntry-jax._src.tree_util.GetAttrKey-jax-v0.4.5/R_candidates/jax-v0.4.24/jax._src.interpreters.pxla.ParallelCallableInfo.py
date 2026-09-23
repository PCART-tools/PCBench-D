@dataclasses.dataclass(frozen=True)
class ParallelCallableInfo:
  name: str
  backend: xc.Client
  axis_name: core.AxisName
  axis_size: int
  global_axis_size: int
  devices: Sequence[xc.Device] | None
  in_axes: Iterable[int | None]
  out_axes_thunk: Callable[[], Sequence[int | None]]
  avals: Sequence[core.AbstractValue]

  @cached_property
  def local_devices(self):
    if self.devices:
      out = [d for d in self.devices
             if d.process_index == xb.process_index(self.backend)]
      assert len(out) > 0
    else:
      out = None  # type: ignore
    return out

  @cached_property
  def out_axes(self):
    return self.out_axes_thunk()
