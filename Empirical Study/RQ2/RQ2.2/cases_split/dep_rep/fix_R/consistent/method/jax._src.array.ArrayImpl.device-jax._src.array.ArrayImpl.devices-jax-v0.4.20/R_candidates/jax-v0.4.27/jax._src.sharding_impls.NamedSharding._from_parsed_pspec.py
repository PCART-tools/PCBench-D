  @classmethod
  def _from_parsed_pspec(
      cls, mesh, parsed_pspec, *, memory_kind=None, _manual_axes=frozenset()
  ):
    return cls(mesh, parsed_pspec.get_partition_spec(),
                memory_kind=memory_kind, _parsed_pspec=parsed_pspec,
                _manual_axes=_manual_axes)
