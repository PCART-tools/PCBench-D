def register_keypaths(
    ty: Type[T], handler: Callable[[T], Tuple[KeyEntry, ...]]
) -> None:
  """[Deprecated] Register the method to get keypaths for type.

  Please use ``register_pytree_with_keys`` instead.

  Only works if the type was already registered with ``register_pytree_node``.
  """
  warnings.warn(
      (
          "jax.tree_util.register_keypaths is deprecated, and will be removed"
          " in a future release. Please use `register_pytree_with_keys()`"
          " instead."
      ),
      category=FutureWarning,
      stacklevel=2,
  )
  _register_keypaths(ty, handler)
