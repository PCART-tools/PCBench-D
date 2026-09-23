class PipelineAllocation(NamedTuple):
  """Allocated VMEM ref and semaphore for an input/output/accum ref."""
  vmem_ref: REF
  semaphore: tpu_core.SemaphoreType
