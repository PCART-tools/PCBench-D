@dataclasses.dataclass(frozen=True)
class SemanticallyEqualShardings:
  shardings: tuple[sharding_impls.GSPMDSharding | UnspecifiedValue, ...]

  def __hash__(self):
    return hash(tuple(
        s._hlo_sharding_hash if isinstance(s, sharding_impls.GSPMDSharding) else s  # type: ignore
        for s in self.shardings))

  def __eq__(self, other):
    if not isinstance(other, SemanticallyEqualShardings):
      return False
    return all(
        (op_shardings.are_op_shardings_equal(s._hlo_sharding, o._hlo_sharding)
         and s.memory_kind == o.memory_kind)
        if (isinstance(s, sharding_impls.GSPMDSharding) and
            isinstance(o, sharding_impls.GSPMDSharding))
        else s == o
        for s, o in zip(self.shardings, other.shardings)
    )
