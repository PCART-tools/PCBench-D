def _child_keys(pytree: Any) -> KeyPath:
  assert not treedef_is_strict_leaf(tree_structure(pytree))
  handler = _registry_with_keypaths.get(type(pytree))
  if handler:
    return tuple(k for k, _ in handler.flatten_with_keys(pytree)[0])
  elif isinstance(pytree, tuple) and hasattr(pytree, '_fields'):
    # handle namedtuple as a special case, based on heuristic
    return tuple(GetAttrKey(s) for s in pytree._fields)
  else:
    num_children = len(treedef_children(tree_structure(pytree)))
    return tuple(FlattenedIndexKey(i) for i in range(num_children))
