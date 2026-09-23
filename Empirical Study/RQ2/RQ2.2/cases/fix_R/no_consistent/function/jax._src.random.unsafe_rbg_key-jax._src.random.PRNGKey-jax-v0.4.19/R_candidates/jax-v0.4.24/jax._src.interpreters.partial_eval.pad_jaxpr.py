def pad_jaxpr(jaxpr: Jaxpr, consts: Sequence[Const]
              ) -> tuple[Jaxpr, list[Const]]:
  bounds = {v: v.aval.dtype.bound for v in jaxpr.invars
            if isinstance(v.aval, core.UnshapedArray) and
            type(v.aval.dtype) is core.bint and not v.aval.shape}
  idxs = {v: DBIdx(i) for i, v in enumerate(jaxpr.invars)}

  def substitute(aval: AbstractValue) -> AbstractValue:
    if (isinstance(aval, core.UnshapedArray) and type(aval.dtype) is core.bint
        and not aval.shape):
      return ShapedArray((), dtypes._scalar_type_to_dtype(int))
    elif isinstance(aval, DShapedArray):
      shape = [bounds.get(d, idxs.get(d, d)) for d in aval.shape]  # type: ignore
      typ = ShapedArray if all(type(d) is int for d in shape) else DShapedArray
      return typ(tuple(shape), aval.dtype, aval.weak_type)
    else:
      return aval

  in_avals = [substitute(v.aval) for v in jaxpr.invars]
  eval_padded = lu.wrap_init(partial(_eval_jaxpr_padded, jaxpr, consts))
  padded_jaxpr, _, padded_consts, () = trace_to_jaxpr_dynamic(eval_padded, in_avals)
  return padded_jaxpr, padded_consts
