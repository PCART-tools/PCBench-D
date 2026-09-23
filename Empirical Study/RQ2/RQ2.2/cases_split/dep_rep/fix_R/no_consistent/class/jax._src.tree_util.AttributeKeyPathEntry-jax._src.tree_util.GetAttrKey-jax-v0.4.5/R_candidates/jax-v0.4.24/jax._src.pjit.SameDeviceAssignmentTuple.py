@dataclasses.dataclass(frozen=True)
class SameDeviceAssignmentTuple:
  shardings: tuple[PjitSharding, ...]
  # device_assignment is Optional because shardings can contain `AUTO` and in
  # that case `mesh` is compulsory to be used. So in that case
  # `_pjit_lower_cached` cache, resource_env will check against the devices.
  device_assignment: XLADeviceAssignment | None

  def __hash__(self):
    shardings_hash = tuple(
        s._hlo_sharding_hash if isinstance(s, GSPMDSharding) else s  # type: ignore
        for s in self.shardings)
    if self.device_assignment is None:
      return hash(shardings_hash)
    else:
      return hash((shardings_hash, *self.device_assignment))

  def __eq__(self, other):
    if not isinstance(other, SameDeviceAssignmentTuple):
      return False
    eq = []
    for s, o in zip(self.shardings, other.shardings):
      s = getattr(s, "_original_sharding", s)
      o = getattr(o, "_original_sharding", o)
      if isinstance(s, GSPMDSharding) and isinstance(o, GSPMDSharding):
        eq.append(
            op_shardings.are_op_shardings_equal(s._hlo_sharding, o._hlo_sharding)
            and s.memory_kind == o.memory_kind)
      else:
        eq.append(s == o)
    return all(eq) and self.device_assignment == other.device_assignment
