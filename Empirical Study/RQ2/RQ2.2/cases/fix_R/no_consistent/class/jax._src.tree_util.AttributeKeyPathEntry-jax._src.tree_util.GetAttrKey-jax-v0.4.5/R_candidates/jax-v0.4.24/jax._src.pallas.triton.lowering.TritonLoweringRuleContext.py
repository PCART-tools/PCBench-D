@dataclasses.dataclass
class TritonLoweringRuleContext:
  context: TritonModuleContext
  avals_in: Any
  avals_out: Any
  block_infos: Sequence[BlockInfo | None]

  @property
  def builder(self) -> tc.builder:
    return tc.builder.current

  replace = dataclasses.replace
