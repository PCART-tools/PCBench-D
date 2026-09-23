def _get_arg_type(
    aval,
    block_mapping: pl_core.BlockMapping | None,
):
  memory_space = None
  if isinstance(aval, pl_core.AbstractMemoryRef):
    memory_space = aval.memory_space
    # We assume unannotated memory refs are in VMEM
    if memory_space is None:
      memory_space = TPUMemorySpace.VMEM
  if isinstance(aval, tpu_core.AbstractSemaphore):
    return aval_to_ir_type(aval), None
  if block_mapping is None:
    return aval_to_ir_type(aval, memory_space=memory_space), aval.shape
  shape = tuple(1 if b is pl_core.mapped else b for b in block_mapping.block_shape)
  return (
      aval_to_ir_type(aval, shape=shape, memory_space=memory_space),
      block_mapping.block_shape,
  )
