@dataclasses.dataclass(frozen=True)
class PipelineCallbackArgs:
  """Args for pipeline prologue and epilogue."""
  pipeline_specs: PipelineArg[PipelineBlockSpecs]
  pipeline_refs: PipelineArg[PipelineRefs]
  pipeline_buffer_refs: PipelineArg[PipelineBuffers]
  pipeline_allocations: PipelineArg[PipelineAllocations]
  pipeline_buffers: PipelineArg[PipelineBuffers]
  make_pipeline_refs: MakePipelineRefs
  start_pipeline_prefetch: StartPipelinePrefetch
