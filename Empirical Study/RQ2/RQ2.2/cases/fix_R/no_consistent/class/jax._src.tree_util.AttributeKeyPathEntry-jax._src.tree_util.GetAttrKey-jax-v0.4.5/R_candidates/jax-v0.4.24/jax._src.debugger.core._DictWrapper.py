@tree_util.register_pytree_node_class
class _DictWrapper:
  keys: list[Hashable]
  values: list[Any]

  def __init__(self, keys, values):
    self._keys = keys
    self._values = values

  def to_dict(self):
    return dict(zip(self._keys, self._values))

  def tree_flatten(self):
    return self._values, self._keys

  @classmethod
  def tree_unflatten(cls, keys, values):
    return _DictWrapper(keys, values)
