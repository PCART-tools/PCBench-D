@dataclasses.dataclass(init=False, unsafe_hash=True)
class BlockSpec:
  index_map: Callable[..., Any] | None
  block_shape: tuple[int | None, ...] | None
  memory_space: Any

  def __init__(self, index_map: Callable[..., Any] | None = None,
               block_shape: tuple[int | None, ...] | None = None,
               memory_space: Any = None):
    self.index_map = index_map
    if block_shape is not None and not isinstance(block_shape, tuple):
      block_shape = tuple(block_shape)
    self.block_shape = block_shape
    self.memory_space = memory_space

  def compute_index(self, *args):
    assert self.index_map is not None
    assert self.block_shape is not None
    out = self.index_map(*args)
    if not isinstance(out, tuple):
      out = (out,)
    return out
