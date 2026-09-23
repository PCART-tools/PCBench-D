class PipelineBody(Protocol):
  """Body of a pipeline."""

  def __call__(self, *ref_args: PipelineRefs) -> None:
    ...
