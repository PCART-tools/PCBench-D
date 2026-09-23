  def __repr__(self):
    mesh_repr = ", ".join(f"'{k}': {v}" for k, v in self.mesh.shape.items())
    mem = '' if self.memory_kind is None else f', memory_kind={self.memory_kind}'
    return f'NamedSharding(mesh=Mesh({mesh_repr}), spec={self.spec}{mem})'
