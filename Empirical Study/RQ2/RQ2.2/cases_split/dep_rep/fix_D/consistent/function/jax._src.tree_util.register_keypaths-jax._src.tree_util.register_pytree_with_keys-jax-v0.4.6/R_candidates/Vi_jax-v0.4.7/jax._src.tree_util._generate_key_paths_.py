def _generate_key_paths_(
    key_path: KeyPath,
    tree: Any,
    is_leaf: Optional[Callable[[Any], bool]] = None,
) -> Iterable[Tuple[KeyPath, Any]]:
  if is_leaf and is_leaf(tree):
    yield key_path, tree
    return
  key_handler = _registry_with_keypaths.get(type(tree))
  handler = _registry.get(type(tree))
  if key_handler:
    key_children, _ = key_handler.flatten_with_keys(tree)
    for k, c in key_children:
      yield from _generate_key_paths_((*key_path, k), c, is_leaf)
  elif handler:
    children, _ = handler.to_iter(tree)
    for i, c in enumerate(children):
      k = FlattenedIndexKey(i)
      yield from _generate_key_paths_((*key_path, k), c, is_leaf)
  elif isinstance(tree, tuple) and hasattr(tree, '_fields'):
    # handle namedtuple as a special case, based on heuristic
    key_children = [(GetAttrKey(s), getattr(tree, s)) for s in tree._fields]
    for k, c in key_children:
      yield from _generate_key_paths_(tuple((*key_path, k)), c, is_leaf)
  else:
    yield key_path, tree  # strict leaf type
