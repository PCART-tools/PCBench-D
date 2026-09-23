def _trace_to_jaxpr_with_refs(f, state_tree: PyTreeDef,
                              state_avals: Sequence[core.AbstractValue]
                              ) -> Tuple[core.Jaxpr, List[Any], PyTreeDef]:
  f, out_tree_thunk = flatten_fun_nokwargs(
      lu.wrap_init(f), treedef_tuple((tree_structure(0), state_tree)))
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      f, state_avals)
  return jaxpr, consts, out_tree_thunk()
