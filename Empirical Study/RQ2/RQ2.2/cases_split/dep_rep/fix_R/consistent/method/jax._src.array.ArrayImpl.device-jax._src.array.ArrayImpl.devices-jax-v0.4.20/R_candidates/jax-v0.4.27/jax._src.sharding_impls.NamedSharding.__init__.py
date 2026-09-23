  @use_cpp_method()
  def __init__(
      self, mesh: mesh_lib.Mesh, spec: PartitionSpec, *,
      memory_kind: str | None = None, _parsed_pspec=None,
      _manual_axes=frozenset()):
    self.mesh = mesh
    self.spec = spec
    self._memory_kind = memory_kind
    self._manual_axes = _manual_axes
    self._parsed_pspec = preprocess(self.mesh, self.spec, _parsed_pspec)
