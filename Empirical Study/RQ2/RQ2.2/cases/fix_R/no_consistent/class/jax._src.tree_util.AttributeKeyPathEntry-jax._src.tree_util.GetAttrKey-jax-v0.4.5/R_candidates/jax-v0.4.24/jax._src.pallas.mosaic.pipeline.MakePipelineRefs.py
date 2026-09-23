class MakePipelineRefs(Protocol):
  """Makes pipeline refs from flat user friendly function args."""

  def __call__(self, *ref_args: PipelineRefs) -> PipelineArg[PipelineRefs]:
    ...
