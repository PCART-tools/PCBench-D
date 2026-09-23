  def __call__(
      self,
      prefetch_args: PipelinePrefetchArgs,
      *,
      force_copy: Union[
          bool, tuple[Union[CondVal, Any], Union[CondVal, Any]]
      ] = False,
      force_skip: Union[
          bool, tuple[Union[CondVal, Any], Union[CondVal, Any]]
      ] = False,
  ) -> tuple[PipelineBuffers, PipelineBuffers]:
    ...
