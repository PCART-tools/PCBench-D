@dataclasses.dataclass
class MeshInfo:
  logical_to_mesh: np.ndarray
  axis_names: list[str]
  mesh_strides: tuple[int, ...]
