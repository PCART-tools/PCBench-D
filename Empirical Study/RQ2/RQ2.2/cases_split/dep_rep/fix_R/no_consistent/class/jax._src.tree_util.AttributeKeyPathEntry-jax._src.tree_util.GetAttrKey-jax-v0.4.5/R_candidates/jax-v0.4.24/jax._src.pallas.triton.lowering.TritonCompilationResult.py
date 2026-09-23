@dataclasses.dataclass
class TritonCompilationResult:
  kernel_name: str
  ttir: str
  ptx: str
  shared_mem_bytes: int
  compute_capability: int
  lowering_result: TritonLoweringResult
