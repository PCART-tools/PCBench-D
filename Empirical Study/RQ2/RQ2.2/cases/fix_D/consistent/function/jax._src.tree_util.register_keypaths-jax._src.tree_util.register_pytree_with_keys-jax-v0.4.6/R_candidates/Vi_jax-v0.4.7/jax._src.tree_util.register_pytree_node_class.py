def register_pytree_node_class(cls: U) -> U:
  """Extends the set of types that are considered internal nodes in pytrees.

  This function is a thin wrapper around ``register_pytree_node``, and provides
  a class-oriented interface::

    @register_pytree_node_class
    class Special:
      def __init__(self, x, y):
        self.x = x
        self.y = y
      def tree_flatten(self):
        return ((self.x, self.y), None)
      @classmethod
      def tree_unflatten(cls, aux_data, children):
        return cls(*children)
  """
  register_pytree_node(cls, op.methodcaller('tree_flatten'), cls.tree_unflatten)
  return cls
