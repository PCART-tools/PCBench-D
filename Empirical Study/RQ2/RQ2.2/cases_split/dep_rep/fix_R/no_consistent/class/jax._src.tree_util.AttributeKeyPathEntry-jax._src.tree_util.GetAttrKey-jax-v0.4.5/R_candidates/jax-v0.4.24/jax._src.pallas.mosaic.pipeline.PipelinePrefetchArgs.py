@dataclasses.dataclass(frozen=True)
class PipelinePrefetchArgs:
  """Args for pipeline prefetch."""
  pipeline_refs: PipelineArg[PipelineRefs]
  pipeline_allocations: PipelineArg[PipelineAllocations]
  pipeline_buffers: PipelineArg[PipelineBuffers]
