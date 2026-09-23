@dataclasses.dataclass
class MeshContext:
  logical_to_mesh: ir.Value
  axis_names: tuple[str, ...]
  mesh_strides: tuple[int, ...]
