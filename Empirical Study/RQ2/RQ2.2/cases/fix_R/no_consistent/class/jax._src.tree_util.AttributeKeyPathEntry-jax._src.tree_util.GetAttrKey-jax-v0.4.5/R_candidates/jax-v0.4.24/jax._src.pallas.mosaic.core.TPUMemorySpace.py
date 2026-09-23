class TPUMemorySpace(enum.Enum):
  ANY = "any"
  VMEM = "vmem"
  SMEM = "smem"
  CMEM = "cmem"
  SEMAPHORE = "semaphore_mem"

  def __str__(self) -> str:
    return self.value

  def __call__(self, shape: tuple[int, ...], dtype: jnp.dtype):
    # A convenience function for constructing MemoryRef types.
    return MemoryRef(shape, dtype, self)
