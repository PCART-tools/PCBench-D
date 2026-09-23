def hoist_consts_to_refs(jaxpr: core.Jaxpr) -> core.Jaxpr:
  all_const_avals = [var.aval for var in jaxpr.constvars]
  is_const_ref = [isinstance(var.aval, AbstractRef) for var in
                  jaxpr.constvars]
  const_avals_, const_ref_avals = partition_list(is_const_ref, all_const_avals)
  const_avals: Sequence[AbstractRef]  = map(AbstractRef, const_avals_)
  merged_const_avals = merge_lists(is_const_ref, const_avals, const_ref_avals)
  arg_avals = [var.aval for var in jaxpr.invars]
  in_avals = [*merged_const_avals, *arg_avals]
  num_consts = len(merged_const_avals)

  def _hoist(*consts_args):
    all_consts, args = split_list(consts_args, [num_consts])
    consts, const_refs = partition_list(is_const_ref, all_consts)
    # We immediately read the const values out of the `Ref`s.
    consts = map(lambda x: ref_get(x, ()), consts)
    all_consts = merge_lists(is_const_ref, consts, const_refs)
    return core.eval_jaxpr(jaxpr, all_consts, *args)
  hoisted_jaxpr, _, consts, () = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(_hoist), in_avals)
  assert not consts, "All consts should have been converted to refs"
  return hoisted_jaxpr
