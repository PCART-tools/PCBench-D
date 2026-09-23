  def call(self, *args_flat) -> Sequence[Any]:
    """Execute on the flat list of arguments, returning flat outputs."""
    # TODO(frostig): improve annotation (sequences of arrays/buffers)
    raise NotImplementedError
