class MakePipelineAllocations(Protocol):
  """Makes pipeline allocations from flat user friendly function args."""

  def __call__(self, *ref_args: PipelineRefs) -> Any:
    ...
