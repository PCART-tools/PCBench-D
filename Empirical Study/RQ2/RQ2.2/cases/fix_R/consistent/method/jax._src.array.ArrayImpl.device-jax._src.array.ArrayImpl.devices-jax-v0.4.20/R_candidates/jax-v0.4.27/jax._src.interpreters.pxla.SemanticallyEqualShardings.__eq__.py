  def __eq__(self, other):
    if not isinstance(other, SemanticallyEqualShardings):
      return False
    return all(
        (op_shardings.are_op_shardings_equal(s._hlo_sharding, o._hlo_sharding)
         and s.memory_kind == o.memory_kind)
        if (isinstance(s, GSPMDSharding) and isinstance(o, GSPMDSharding))
        else s == o
        for s, o in zip(self._gspmd_shardings, other._gspmd_shardings)
    )
