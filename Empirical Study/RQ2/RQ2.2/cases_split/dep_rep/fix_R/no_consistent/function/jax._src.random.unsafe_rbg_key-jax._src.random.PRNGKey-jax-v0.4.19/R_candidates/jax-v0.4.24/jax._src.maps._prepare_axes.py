def _prepare_axes(axes, arg_name):
  entries, treedef = tree_flatten(axes, is_leaf=_is_axes_leaf)
  entries = map(partial(_parse_entry, arg_name), entries)
  return tree_unflatten(treedef, entries), entries, treedef
