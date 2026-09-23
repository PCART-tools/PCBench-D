class AxisEnv(NamedTuple):
  """Represents a pmap mesh (only along the replica axes)."""
  nreps: int
  names: tuple[Any, ...]
  sizes: tuple[int, ...]
