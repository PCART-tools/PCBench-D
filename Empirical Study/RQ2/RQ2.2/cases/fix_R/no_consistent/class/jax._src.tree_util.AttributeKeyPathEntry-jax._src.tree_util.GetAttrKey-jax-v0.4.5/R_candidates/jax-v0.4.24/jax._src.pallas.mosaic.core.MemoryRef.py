@dataclasses.dataclass(frozen=True)
class MemoryRef:
  """Like jax.ShapeDtypeStruct but with memory spaces."""
  shape: tuple[int, ...]
  dtype: jnp.dtype
  memory_space: TPUMemorySpace = TPUMemorySpace.ANY

  def get_aval(self) -> AbstractMemoryRef:
    return AbstractMemoryRef(
        jax_core.ShapedArray(self.shape, self.dtype), self.memory_space)
