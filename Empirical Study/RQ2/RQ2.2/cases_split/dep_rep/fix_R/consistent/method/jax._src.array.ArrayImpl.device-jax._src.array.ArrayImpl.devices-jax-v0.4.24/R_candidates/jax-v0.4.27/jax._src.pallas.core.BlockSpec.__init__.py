  def __init__(self, index_map: Callable[..., Any] | None = None,
               block_shape: tuple[int | None, ...] | None = None,
               memory_space: Any = None, indexing_mode: IndexingMode = blocked):
    self.index_map = index_map
    if block_shape is not None and not isinstance(block_shape, tuple):
      block_shape = tuple(block_shape)
    self.block_shape = block_shape
    self.memory_space = memory_space
    self.indexing_mode = indexing_mode
