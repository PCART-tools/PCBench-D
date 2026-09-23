def aval_to_ir_type(aval, shape=None, memory_space: TPUMemorySpace | None = None):
  if isinstance(aval, tpu_core.AbstractSemaphore):
    if aval.sem_type is tpu_core.SemaphoreType.DMA:
      sem_type = ir.Type.parse("!tpu.dma_semaphore")
    elif aval.sem_type is tpu_core.SemaphoreType.REGULAR:
      sem_type = ir.Type.parse("!tpu.semaphore")
    elif aval.sem_type is tpu_core.SemaphoreType.BARRIER:
      sem_type = ir.Type.parse("!tpu.semaphore")
    else:
      raise ValueError(f"Cannot allocate {aval.sem_type}.")
    memspace = _memory_space_to_tpu_memspace(TPUMemorySpace.SEMAPHORE)
    return ir.MemRefType.get((), sem_type, memory_space=memspace)
  if isinstance(aval, state.AbstractRef):
    if shape is None:
      shape = aval.shape
    memspace = _memory_space_to_tpu_memspace(memory_space)
    return ir.MemRefType.get(shape, _dtype_to_ir_type(aval.dtype),
                             memory_space=memspace)
  if isinstance(aval, jax_core.ShapedArray):
    if shape is None:
      shape = aval.shape
    if not shape:
      return _dtype_to_ir_type(aval.dtype)
    return ir.VectorType.get(shape, _dtype_to_ir_type(aval.dtype))
  raise NotImplementedError(aval)
