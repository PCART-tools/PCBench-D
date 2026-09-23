def build_tree(treedef: PyTreeDef, xs: Any) -> Any:
  return treedef.from_iterable_tree(xs)
