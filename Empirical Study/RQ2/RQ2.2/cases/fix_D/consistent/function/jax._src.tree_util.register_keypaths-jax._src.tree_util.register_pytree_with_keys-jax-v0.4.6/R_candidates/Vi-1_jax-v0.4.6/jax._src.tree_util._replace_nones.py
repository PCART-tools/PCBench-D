def _replace_nones(sentinel, tree):
  """Replaces ``None`` in ``tree`` with ``sentinel``."""
  if tree is None:
    return sentinel
  else:
    handler = _registry.get(type(tree))
    if handler:
      children, metadata = handler.to_iter(tree)
      proc_children = [_replace_nones(sentinel, child) for child in children]
      return handler.from_iter(metadata, proc_children)
    elif isinstance(tree, tuple) and hasattr(tree, '_fields'):
      # handle namedtuple as a special case, based on heuristic
      children = iter(tree)
      proc_children = [_replace_nones(sentinel, child) for child in children]
      return type(tree)(*proc_children)
    else:
      return tree
