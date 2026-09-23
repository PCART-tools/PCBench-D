def flatten_one_level(pytree: Any) -> Tuple[List[Any], Hashable]:
  handler = _registry.get(type(pytree))
  if handler:
    children, meta = handler.to_iter(pytree)
    return list(children), meta
  elif isinstance(pytree, tuple) and hasattr(pytree, '_fields'):
    return list(pytree), None
  else:
    raise ValueError(f"can't tree-flatten type: {type(pytree)}")
