def substitute_vars_in_output_ty(
    out_type: Sequence[AbstractValue],  # shapes may contain InDBIdx / OutDBIdx
    in_atoms: Sequence[Atom],
    out_binders: Sequence[Var],
  ) -> List[AbstractValue]:  # shapes may contain Vars
  in_atoms = [x.val if type(x) is Literal else x for x in in_atoms]
  result = []
  for aval in out_type:
    if type(aval) is DShapedArray:
      shape = [in_atoms[d.val] if type(d) is InDBIdx else  # type: ignore
               out_binders[d.val] if type(d) is OutDBIdx else  # type: ignore
               d for d in aval.shape]
      aval = aval.update(shape=tuple(shape))
    result.append(aval)
  return result
