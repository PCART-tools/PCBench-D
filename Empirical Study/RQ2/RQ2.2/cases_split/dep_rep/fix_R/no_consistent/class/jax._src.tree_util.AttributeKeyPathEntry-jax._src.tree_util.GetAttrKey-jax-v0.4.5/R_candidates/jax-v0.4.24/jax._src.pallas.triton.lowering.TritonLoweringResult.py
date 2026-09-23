@dataclasses.dataclass
class TritonLoweringResult:
  """Keeps pybind11 objects alive."""

  module: ir.Module
  grid: tuple[int, ...]
