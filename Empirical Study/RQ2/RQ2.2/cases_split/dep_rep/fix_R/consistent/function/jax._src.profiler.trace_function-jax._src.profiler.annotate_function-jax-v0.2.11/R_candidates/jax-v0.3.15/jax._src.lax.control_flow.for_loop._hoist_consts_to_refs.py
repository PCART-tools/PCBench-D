def _hoist_consts_to_refs(jaxpr: core.Jaxpr) -> core.Jaxpr:
  num_consts = len(jaxpr.constvars)

  # Note that this function is meant for use w/ `for_loop` since it assumes
  # that the index is the first argument and preserves this after hoisting
  # consts.
  def _hoist(i, *consts_args):
    const_refs, args = split_list(consts_args, [num_consts])
    # We immediately read the const values out of the `Ref`s.
    consts = [r[()] for r in const_refs]
    return core.eval_jaxpr(jaxpr, consts, i, *args)
  assert all(isinstance(var.aval, core.ShapedArray) for var in jaxpr.constvars)
  const_avals = [ShapedArrayRef(var.aval.shape, var.aval.dtype) for var in  # pytype: disable=attribute-error
                 jaxpr.constvars]
  i_aval, *arg_avals = [var.aval for var in jaxpr.invars]
  in_avals = [i_aval, *const_avals, *arg_avals]
  hoisted_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(_hoist), in_avals)
  assert not consts, "All consts should have been converted to refs"
  return hoisted_jaxpr
