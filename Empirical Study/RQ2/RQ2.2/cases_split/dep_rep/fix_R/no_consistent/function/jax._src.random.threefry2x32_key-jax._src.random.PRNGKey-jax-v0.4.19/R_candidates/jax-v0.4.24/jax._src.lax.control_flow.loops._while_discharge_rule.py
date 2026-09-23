def _while_discharge_rule(in_avals, out_avals, *args, cond_jaxpr, body_jaxpr,
                          cond_nconsts, body_nconsts):
  # TODO(sharadmv): enable supporting state effects in the cond
  if any(isinstance(eff, state.RefEffect) for eff in cond_jaxpr.effects):
    raise NotImplementedError
  cond_consts, body_consts, carry = split_list(args, [cond_nconsts, body_nconsts])
  cond_consts_avals, body_consts_avals, carry_avals = split_list(in_avals,
                                                                 [cond_nconsts,
                                                                  body_nconsts])
  # There shouldn't be any `Ref`s in the `cond` (because of our check above).
  assert not any(isinstance(aval, state.AbstractRef) for aval in cond_consts_avals)
  is_ref = [isinstance(aval, state.AbstractRef) for aval in body_consts_avals]
  remaining_body_consts, refs = partition_list(is_ref, body_consts)
  remaining_body_const_avals, ref_avals = partition_list(is_ref,
                                                         body_consts_avals)
  num_refs = sum(is_ref)
  num_remaining_consts = body_nconsts - num_refs
  num_carry = len(in_avals) - body_nconsts - cond_nconsts
  body_jaxpr, body_jaxpr_consts = body_jaxpr.jaxpr, body_jaxpr.consts
  cond_jaxpr, cond_jaxpr_consts = cond_jaxpr.jaxpr, cond_jaxpr.consts
  if body_jaxpr_consts:
    raise NotImplementedError("Body jaxpr has consts. If you see this error, "
                              "please open an issue at "
                              "https://github.com/google/jax/issues")
  # body_jaxpr has the signature (*body_consts, *carry) -> carry.
  # Some of these body_consts are actually `Ref`s so when we discharge
  # them, they also turn into outputs, effectively turning those consts into
  # carries. However this doesn't fit the expected signature for the body_jaxpr.
  # Therefore we need to rewrite the jaxpr to shuffle around the `Ref`s so that
  # they are part of the carry.
  discharged_body_jaxpr, discharged_consts = state_discharge.discharge_state(
      body_jaxpr, ())
  if discharged_consts: raise NotImplementedError

  def new_body(*consts_refs_carry):
    consts, refs, carry = split_list(
        consts_refs_carry, [num_remaining_consts, num_refs])
    consts_and_refs = merge_lists(is_ref, consts, refs)
    carry_refs = core.eval_jaxpr(discharged_body_jaxpr, (), *consts_and_refs,
                                 *carry)
    carry, refs_out = split_list(carry_refs, [num_carry])
    return [*refs_out, *carry]
  new_body_jaxpr, _, new_body_consts, () = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(new_body), [*remaining_body_const_avals, *[a.inner_aval for a
                                                              in ref_avals],
                               *carry_avals])
  if new_body_consts: raise NotImplementedError

  # Since some `Ref`s that were previously consts are now carries, we need to
  # deal with them (i.e. ignore them) in the `cond`, so we need to rewrite the
  # cond_jaxpr as well.
  def new_cond(*consts_refs_carry):
    consts, refs, carry = split_list(
        consts_refs_carry, [cond_nconsts, num_refs])
    del refs  # We don't use them here!
    return core.eval_jaxpr(cond_jaxpr, cond_jaxpr_consts, *consts, *carry)
  new_cond_jaxpr, _, new_cond_consts, () = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(new_cond), [*cond_consts_avals,
                               *[a.inner_aval for a in ref_avals],
                               *carry_avals])
  if new_cond_consts: raise NotImplementedError

  out = while_p.bind(*cond_consts, *remaining_body_consts, *refs, *carry,
                     body_jaxpr=core.ClosedJaxpr(new_body_jaxpr, ()),
                     cond_jaxpr=core.ClosedJaxpr(new_cond_jaxpr, ()),
                     body_nconsts=num_remaining_consts,
                     cond_nconsts=cond_nconsts)
  refs_out, carry_out = split_list(out, [num_refs])
  updated_body_consts = merge_lists(is_ref, [None] * num_remaining_consts,
                                    refs_out)
  invals_out = [
      *[None] * cond_nconsts,
      *updated_body_consts,
      *[None] * num_carry]
  return invals_out, carry_out
