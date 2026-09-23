def _reshape_typecheck_rule(operand, *dyn_shape, new_sizes, dimensions):
  if not dyn_shape:
    out_aval, effects = reshape_p.abstract_eval(
        operand.aval, new_sizes=new_sizes, dimensions=dimensions)
    return [out_aval], effects
  else:
    # TODO(mattjj, necula): perform more checks like _reshape_shape_rule
    out_shape = _merge_dyn_shape(new_sizes, dyn_shape)
    out_shape = [x.val if type(x) is core.Literal else x for x in out_shape]
    out_aval = core.DShapedArray(tuple(out_shape), operand.aval.dtype,
                                 operand.aval.weak_type)
    return [out_aval], core.no_effects
