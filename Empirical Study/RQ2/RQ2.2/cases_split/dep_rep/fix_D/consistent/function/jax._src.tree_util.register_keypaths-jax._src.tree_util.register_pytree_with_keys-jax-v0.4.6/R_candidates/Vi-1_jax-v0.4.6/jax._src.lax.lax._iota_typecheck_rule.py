def _iota_typecheck_rule(*dyn_shape, dtype, shape, dimension):
  if not dyn_shape:
    out_aval, effects = iota_p.abstract_eval(
        dtype=dtype, shape=shape, dimension=dimension)
    return [out_aval], effects
  else:
    out_shape = _merge_dyn_shape(shape, dyn_shape)
    out_shape = [x.val if type(x) is core.Literal else x for x in out_shape]  # pytype: disable=attribute-error
    out_aval = core.DShapedArray(tuple(out_shape), dtype, False)
    return [out_aval], core.no_effects
