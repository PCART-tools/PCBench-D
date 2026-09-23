  def __call__(
      self,
      *ref_args: PipelineRefs,
      scratchs: PipelineRefs = None,
      allocations: Union[None, Any] = None,
      init_allocations: CondVal = False,
      prologue: Union[PipelinePrologue, None] = None,
      epilogue: Union[PipelineEpilogue, None] = None,
      out_prologue: Union[PipelineOutPrologue, None] = None,
      out_epilogue: Union[PipelineOutEpilogue, None] = None,
  ) -> None:
    ...
