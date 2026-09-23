def _child_keys(pytree: Any) -> List[KeyPathEntry]:
  assert not treedef_is_strict_leaf(tree_structure(pytree))
  handler = _keypath_registry.get(type(pytree))
  if handler:
    return handler(pytree)
  elif isinstance(pytree, tuple) and hasattr(pytree, '_fields'):
    # handle namedtuple as a special case, based on heuristic
    return [AttributeKeyPathEntry(s) for s in pytree._fields]
  else:
    num_children = len(treedef_children(tree_structure(pytree)))
    return [FlattenedKeyPathEntry(i) for i in range(num_children)]
