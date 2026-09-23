def treedef_tuple(treedefs: Iterable[PyTreeDef]) -> PyTreeDef:
  """Makes a tuple treedef from an iterable of child treedefs."""
  return pytree.tuple(list(treedefs))
