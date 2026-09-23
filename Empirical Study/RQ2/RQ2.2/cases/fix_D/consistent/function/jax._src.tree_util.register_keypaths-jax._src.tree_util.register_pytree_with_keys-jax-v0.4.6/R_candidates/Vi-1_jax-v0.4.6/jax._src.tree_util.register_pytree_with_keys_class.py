def register_pytree_with_keys_class(cls: U) -> U:
  """Extends the set of types that are considered internal nodes in pytrees.

  This function is similar to ``register_pytree_node_class``, but requires a
  class that defines how it could be flattened with keys.

  It is a thin wrapper around ``register_pytree_with_keys``, and
  provides a class-oriented interface::

    @register_pytree_with_keys_class
    class Special:
      def __init__(self, x, y):
        self.x = x
        self.y = y
      def tree_flatten_with_keys(self):
        return (((GetAttrKey('x'), self.x), (GetAttrKey('y'), self.y)), None)
      @classmethod
      def tree_unflatten(cls, aux_data, children):
        return cls(*children)
  """
  register_pytree_with_keys(
      cls, op.methodcaller("tree_flatten_with_keys"), cls.tree_unflatten
  )
  return cls
