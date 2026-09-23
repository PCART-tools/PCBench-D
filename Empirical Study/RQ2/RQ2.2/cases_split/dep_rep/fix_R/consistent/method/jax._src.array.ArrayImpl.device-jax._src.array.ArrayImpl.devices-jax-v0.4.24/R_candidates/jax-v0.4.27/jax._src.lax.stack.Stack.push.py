  def push(self, elem: Any) -> Stack:
    """Pushes `elem` onto the stack, returning the updated stack."""
    return Stack(
      self._size + 1,
      jax.tree_util.tree_map(
        lambda x, y: lax.dynamic_update_index_in_dim(x, y, self._size, 0),
        self._data, elem))
