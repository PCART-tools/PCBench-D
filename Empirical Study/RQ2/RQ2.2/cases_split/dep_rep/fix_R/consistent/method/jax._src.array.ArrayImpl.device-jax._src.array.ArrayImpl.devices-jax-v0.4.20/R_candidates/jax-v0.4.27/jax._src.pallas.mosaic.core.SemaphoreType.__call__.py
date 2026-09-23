  def __call__(self, shape: tuple[int, ...]):
    if self == SemaphoreType.DMA:
      dtype = DmaSemaphoreTy()
    elif self == SemaphoreType.BARRIER:
      dtype = BarrierSemaphoreTy()
    else:
      dtype = SemaphoreTy()
    return MemoryRef(shape, dtype, TPUMemorySpace.SEMAPHORE)
