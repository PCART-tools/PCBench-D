class CompiledCallParams(NamedTuple):
  executable: Executable
  no_kwargs: bool
  in_tree: tree_util.PyTreeDef
  out_tree: tree_util.PyTreeDef
