  def __call__(
      self,
      prefetch_args: ManualPrefetchArgs,
      *,
      indices: GridIndices,
      force_copy: Union[bool, Union[CondVal, Any]] = False,
      force_skip: Union[bool, Union[CondVal, Any]] = False,
  ) -> PipelineBuffers:
    ...
