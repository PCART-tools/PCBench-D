def register_keypaths(
    ty: type[T], handler: Callable[[T], tuple[KeyEntry, ...]]
) -> None:
  """[Deprecated] Register the method to get keypaths for type.

  Please use ``register_pytree_with_keys`` instead.

  Only works if the type was already registered with ``register_pytree_node``.
  """
  _register_keypaths(ty, handler)
