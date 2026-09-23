@dataclasses.dataclass(frozen=True)
class TileManual:
  manual_axes: frozenset[sharding_impls.MeshAxisName]
