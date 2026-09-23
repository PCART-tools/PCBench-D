def discharged_for_loop(nsteps, body, init_state, *, reverse: bool = False):
  """A `for_loop` implementation that discharges its body right away.

  Potentially useful for testing and benchmarking.
  """
  flat_state, state_tree = tree_flatten(init_state)
  state_avals = map(state_utils.val_to_ref_aval, flat_state)
  idx_aval = core.ShapedArray((), jnp.dtype("int32"))
  jaxpr, consts, out_tree = _trace_to_jaxpr_with_refs(
      body, state_tree, [idx_aval, *state_avals])
  if out_tree != tree_structure(None):
    raise Exception("`body` should not return anything.")
  discharged_jaxpr, discharged_consts = discharge_state(jaxpr, consts)

  def fori_body(i, carry):
    i = jnp.int32(i)
    if reverse:
      i = nsteps - i - 1
    out_flat = core.eval_jaxpr(discharged_jaxpr, discharged_consts,
                               i, *carry)
    return out_flat
  out_flat = loops.fori_loop(0, nsteps, fori_body, flat_state)
  return tree_unflatten(state_tree, out_flat)
