class StartPipelinePrefetch(Protocol):
  """Starts pipeline prefetch.

  Use force_copy if a spec's indices don't change from last to first grid
  indices and you still want to force a copy. This must be used in conjunction
  with the prologue's return value to force a wait.
  """

  def __call__(
      self,
      prefetch_args: PipelinePrefetchArgs,
      *,
      force_copy: Union[
          bool, tuple[Union[CondVal, Any], Union[CondVal, Any]]
      ] = False,
  ) -> PipelineArg[PipelineBuffers]:
    ...
