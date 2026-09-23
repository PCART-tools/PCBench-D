def flatten_one_level(pytree: Any) -> Tuple[List[Any], Hashable]:
  """Flatten the given pytree node by one level.

  Args:
    pytree: A valid pytree node, either built-in or registered via
      ``register_pytree_node`` or ``register_pytree_with_keys``.

  Returns:
    A pair of the pytree's flattened children and its hashable metadata.

  Raises:
    ValueError: If the given pytree is not a built-in or registered container
    via ``register_pytree_node`` or ``register_pytree_with_keys``.
  """
  handler = _registry.get(type(pytree))
  if handler:
    children, meta = handler.to_iter(pytree)
    return list(children), meta
  elif isinstance(pytree, tuple) and hasattr(pytree, '_fields'):
    # handle namedtuple as a special case, based on heuristic
    return [getattr(pytree, s) for s in pytree._fields], None
  else:
    raise ValueError(f"can't tree-flatten type: {type(pytree)}")
