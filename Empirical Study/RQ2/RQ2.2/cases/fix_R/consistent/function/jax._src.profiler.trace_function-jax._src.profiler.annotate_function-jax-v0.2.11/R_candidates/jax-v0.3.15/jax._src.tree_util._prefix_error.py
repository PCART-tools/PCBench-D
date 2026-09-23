def _prefix_error(key_path: KeyPath, prefix_tree: Any, full_tree: Any,
                  is_leaf: Optional[Callable[[Any], bool]] = None,
                  ) -> Iterable[Callable[[str], ValueError]]:
  # A leaf is a valid prefix of any tree:
  if treedef_is_strict_leaf(tree_structure(prefix_tree, is_leaf=is_leaf)): return

  # The subtrees may disagree because their roots are of different types:
  if type(prefix_tree) != type(full_tree):
    yield lambda name: ValueError(
      "pytree structure error: different types at key path\n"
      f"    {{name}}{key_path.pprint()}\n"
      f"At that key path, the prefix pytree {{name}} has a subtree of type\n"
      f"    {type(prefix_tree)}\n"
      f"but at the same key path the full pytree has a subtree of different type\n"
      f"    {type(full_tree)}.".format(name=name))
    return  # don't look for more errors in this subtree

  # Or they may disagree if their roots have different numbers of children (note
  # that because both prefix_tree and full_tree have the same type at this
  # point, and because prefix_tree is not a leaf, each can be flattened once):
  prefix_tree_children, prefix_tree_meta = flatten_one_level(prefix_tree)
  full_tree_children, full_tree_meta = flatten_one_level(full_tree)
  if len(prefix_tree_children) != len(full_tree_children):
    yield lambda name: ValueError(
      "pytree structure error: different numbers of pytree children at key path\n"
      f"    {{name}}{key_path.pprint()}\n"
      f"At that key path, the prefix pytree {{name}} has a subtree of type\n"
      f"    {type(prefix_tree)}\n"
      f"with {len(prefix_tree_children)} children, "
      f"but at the same key path the full pytree has a subtree of the same "
      f"type but with {len(full_tree_children)} children.".format(name=name))
    return  # don't look for more errors in this subtree

  # Or they may disagree if their roots have different pytree metadata:
  if prefix_tree_meta != full_tree_meta:
    prefix_tree_meta_str = str(prefix_tree_meta)
    full_tree_meta_str = str(full_tree_meta)
    metadata_diff = textwrap.indent(
        '\n'.join(difflib.ndiff(prefix_tree_meta_str.splitlines(),
                                full_tree_meta_str.splitlines())),
        prefix="    ")
    yield lambda name: ValueError(
      "pytree structure error: different pytree metadata at key path\n"
      f"    {{name}}{key_path.pprint()}\n"
      f"At that key path, the prefix pytree {{name}} has a subtree of type\n"
      f"    {type(prefix_tree)}\n"
      f"with metadata\n"
      f"    {prefix_tree_meta_str}\n"
      f"but at the same key path the full pytree has a subtree of the same "
      f"type but with metadata\n"
      f"    {full_tree_meta_str}\n"
      f"so the diff in the metadata at these pytree nodes is\n"
      f"{metadata_diff}".format(name=name))
    return  # don't look for more errors in this subtree

  # If the root types and numbers of children agree, there must be an error
  # in a subtree, so recurse:
  keys = _child_keys(prefix_tree)
  keys_ = _child_keys(full_tree)
  assert keys == keys_, \
    f"equal pytree nodes gave differing keys: {keys} and {keys_}"
  for k, t1, t2 in zip(keys, prefix_tree_children, full_tree_children):
    yield from _prefix_error(key_path + k, t1, t2)
