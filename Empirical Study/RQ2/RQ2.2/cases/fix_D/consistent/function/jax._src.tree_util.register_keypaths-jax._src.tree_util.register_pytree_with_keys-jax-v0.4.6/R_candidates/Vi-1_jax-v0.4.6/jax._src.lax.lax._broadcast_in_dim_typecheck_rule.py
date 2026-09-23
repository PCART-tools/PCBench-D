def _broadcast_in_dim_typecheck_rule(
    operand, *dyn_shape, shape, broadcast_dimensions):
  if not dyn_shape:
    out_aval, effects = broadcast_in_dim_p.abstract_eval(
        operand.aval, shape=shape, broadcast_dimensions=broadcast_dimensions)
    return [out_aval], effects
  else:
    # TODO(mattjj): perform more checks like _broadcast_in_dim_shape_rule
    out_shape = _merge_dyn_shape(shape, dyn_shape)
    out_shape = [x.val if type(x) is core.Literal else x for x in out_shape]  # pytype: disable=attribute-error
    out_aval = core.DShapedArray(tuple(out_shape), operand.aval.dtype,
                                 operand.aval.weak_type)
    return [out_aval], core.no_effects
