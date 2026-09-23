@tree_util.register_pytree_node_class
@dataclasses.dataclass
class Slice:
  """Represents a slice with a dynamic start index and a fixed size."""
  start: Any
  size: int

  def __post_init__(self):
    if self.size < 0:
      raise ValueError("`size` must not be negative.")

  def tree_flatten(self):
    # If `start` is statically known, we treat it as static information
    if isinstance(self.start, int):
      return (), (self.start, self.size)
    return (self.start,), (self.size,)

  @classmethod
  def tree_unflatten(cls, aux_data, children) -> Slice:
    return cls(*children, *aux_data)

  @classmethod
  def from_slice(cls, slc: slice, size: int) -> Slice:
    start, stop, step = slc.indices(size)
    if step != 1:
      raise ValueError(f"slice must have a step of 1 (found: {step})")
    return cls(start, max(stop - start, 0))
