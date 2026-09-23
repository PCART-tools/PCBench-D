def _scan_state_discharge_rule(in_avals, out_avals, *args, jaxpr, num_consts,
                               num_carry, linear, unroll, reverse, length):
  jaxpr, consts = jaxpr.jaxpr, jaxpr.consts
  if consts: raise NotImplementedError
  consts, carry, xs = split_list(args, [num_consts, num_carry])
  consts_linear, carry_linear, xs_linear = split_list(
      linear, [num_consts, num_carry])
  consts_avals, carry_avals, xs_avals = split_list(in_avals,
                                                   [num_consts, num_carry])
  is_ref = [isinstance(a, state.AbstractRef) for a in consts_avals]
  remaining_const_avals, in_ref_avals = partition_list(is_ref, consts_avals)
  remaining_consts, in_refs = partition_list(is_ref, consts)
  remaining_consts_linear, in_refs_linear = partition_list(is_ref, consts_linear)
  num_refs = sum(is_ref)
  num_extensive_in = len(in_avals) - num_carry - num_consts
  num_extensive_out = len(out_avals) - num_carry
  num_remaining_consts = num_consts - num_refs
  discharged_jaxpr, discharged_consts = state_discharge.discharge_state(jaxpr, ())
  if discharged_consts:
    raise NotImplementedError("Discharged jaxpr has consts. If you see this, "
                              "please open an issue at "
                              "https://github.com/google/jax/issues")
  # The discharged jaxpr will have output refs stashed at the end
  def wrapped(*refs_and_args):
    consts, refs, carry, xs = split_list(refs_and_args, [num_remaining_consts,
                                                         num_refs,
                                                         num_carry])
    consts_with_refs = merge_lists(is_ref, consts, refs)
    outs_and_refs = core.eval_jaxpr(discharged_jaxpr, (), *consts_with_refs,
                                    *carry, *xs)
    carry, ys, out_refs = split_list(outs_and_refs, [num_carry,
                                                     num_extensive_out])
    assert len(out_refs) == num_refs
    return [*out_refs, *carry, *ys]
  new_in_avals = [*remaining_const_avals, *[a.inner_aval for a in in_ref_avals],
                  *carry_avals,
                  *[core.mapped_aval(length, 0, a) for a in xs_avals]]
  new_jaxpr, _, (), () = pe.trace_to_jaxpr_dynamic(lu.wrap_init(wrapped), new_in_avals)
  new_linear = (*remaining_consts_linear, *in_refs_linear,
                *carry_linear, *xs_linear)
  all_out = scan_p.bind(*remaining_consts, *in_refs, *carry, *xs,
                        jaxpr=core.ClosedJaxpr(new_jaxpr, ()),
                        length=length,
                        num_consts=num_remaining_consts,
                        num_carry=num_refs + num_carry,
                        unroll=unroll,
                        reverse=reverse,
                        linear=new_linear)
  refs_out, carry_out, ys_out = split_list(all_out, [num_refs, num_carry])
  new_invals = [*merge_lists(is_ref, [None] * num_remaining_consts, refs_out),
                *[None] * num_carry, *[None] * num_extensive_in]
  assert len(new_invals) == len(in_avals)
  return new_invals, [*carry_out, *ys_out]
