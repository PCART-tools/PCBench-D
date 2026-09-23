def xeinsum(spec: str, *operands):
  in_spec, out_spec = spec.split('->')
  all_in_subs, all_in_named = unzip2(XeinsumSpecParser(in_spec).parse_args())
  (out_subs, out_named), = XeinsumSpecParser(out_spec).parse_args()

  if len(operands) != len(all_in_named):
    raise ValueError("Expecting the same number of argument specs in the "
                     "subscript ({in_spec}) as the number of operands. But got "
                     "{len(all_in_named)} argument specs for "
                     "{len(operands)} operands")

  if len(operands) > 2:
    raise NotImplementedError("Only one or two operands are supported. "
                              f"But got {len(operands)} operands")

  # output subs and named axes must appear in at least one of the inputs.
  if not set(out_named).issubset(set().union(*all_in_named)):
    raise ValueError("Found named axes "
                     f"{set(out_named) - set().union(*all_in_named)} "
                     "appearing in the output spec but not in the input")
  if not set(out_subs).issubset(set().union(*all_in_subs)):
    raise ValueError("Found subscript(s) "
                     f"{set(out_subs) - set().union(*all_in_subs)} "
                     "appearing in the output spec but not in the input")

  xs = list(operands)
  for idx, (in_subs, in_named) in enumerate(safe_zip(all_in_subs, all_in_named)):
    # if a subscript axis appears only in one input and not the output, reduce!
    other_named = set().union(  # type: ignore
        *[named for i, named in enumerate(all_in_named) if i != idx])
    other_subs = set().union(  # type: ignore
        *[subs for i, subs in enumerate(all_in_subs) if i != idx])

    subs_reduce = list(set(in_subs) - {*out_subs, *other_subs})
    subs_reduce_axes = [in_subs.index(n) for n in subs_reduce]
    named_reduce_axes = list(set(in_named) - {*out_named, *other_named})

    if subs_reduce_axes or named_reduce_axes:
      xs[idx] = psum(xs[idx], axis_name=subs_reduce_axes + named_reduce_axes)
      for i in sorted(subs_reduce_axes, reverse=True):
        del all_in_subs[idx][i]
      for named_axis in named_reduce_axes:
        all_in_named[idx].remove(named_axis)

  if len(operands) == 1:
    return xs[0]

  if len(operands) == 2:
    x, y = xs
    lhs_subs, rhs_subs = all_in_subs
    lhs_named, rhs_named = all_in_named

    # if a named axis appears in both inputs and not the output, contract!
    named_contract = list((set(lhs_named) & set(rhs_named)) - set(out_named))

    # if a subscript appears in both inputs and not the outputs, contract!
    subs_contract = (set(lhs_subs) & set(rhs_subs)) - set(out_subs)

    pos_contract = unzip2((lhs_subs.index(n), rhs_subs.index(n))
                          for n in subs_contract)

    # if a subscript appears in both inputs _and_ the outputs, batch!
    subs_batch = (set(lhs_subs) & set(rhs_subs)) - subs_contract
    pos_batch = unzip2((lhs_subs.index(n), rhs_subs.index(n)) for n in subs_batch)

    return pdot(x, y, axis_name=named_contract,
                pos_contract=pos_contract, pos_batch=pos_batch)
