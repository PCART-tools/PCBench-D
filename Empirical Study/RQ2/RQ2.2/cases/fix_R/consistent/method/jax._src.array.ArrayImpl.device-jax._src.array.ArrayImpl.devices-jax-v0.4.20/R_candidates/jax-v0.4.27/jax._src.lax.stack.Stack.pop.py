  def pop(self) -> tuple[Any, Stack]:
    """Pops from the stack, returning an (elem, updated stack) pair."""
    elem = jax.tree_util.tree_map(
      lambda x: lax.dynamic_index_in_dim(x, self._size - 1, 0, keepdims=False),
      self._data)
    return elem, Stack(self._size - 1, self._data)
