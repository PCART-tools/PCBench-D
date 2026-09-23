def treedef_tuple(treedefs: Iterable[PyTreeDef]) -> PyTreeDef:
  """Makes a tuple treedef from an iterable of child treedefs."""
  if default_registry:
    return pytree.tuple(default_registry, list(treedefs))  # type: ignore
  else:
    return pytree.tuple(list(treedefs))  # type: ignore
