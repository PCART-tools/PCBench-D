  def __hash__(self):
    return hash(tuple(
        (s._hlo_sharding_hash, s.memory_kind)  # type: ignore
        if isinstance(s, GSPMDSharding) else s for s in self._gspmd_shardings))
