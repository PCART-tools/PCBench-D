@dataclasses.dataclass
class TritonModuleContext:
  name: str
  grid_mapping: GridMapping
  program_ids: Sequence[tc.tensor]
