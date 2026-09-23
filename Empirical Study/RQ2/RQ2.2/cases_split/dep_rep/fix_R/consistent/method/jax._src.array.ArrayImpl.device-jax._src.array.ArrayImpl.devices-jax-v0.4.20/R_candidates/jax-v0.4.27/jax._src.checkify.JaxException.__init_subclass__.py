  def __init_subclass__(cls):
    jtu.register_pytree_node_class(cls)
