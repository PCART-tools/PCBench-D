def standard_abstract_eval(prim, shape_rule, dtype_rule, weak_type_rule,
                           named_shape_rule, *avals, **kwargs):
  assert all(isinstance(aval, core.UnshapedArray) for aval in avals), avals
  assert not prim.multiple_results
  weak_type = weak_type_rule(*avals, **kwargs)
  least_specialized = _max(map(type, avals),
                           key=operator.attrgetter('array_abstraction_level'))
  if least_specialized is core.ConcreteArray:
    out = prim.impl(*[x.val for x in avals], **kwargs)
    return core.ConcreteArray(out.dtype, out, weak_type=weak_type)
  elif least_specialized is core.ShapedArray:
    return core.ShapedArray(shape_rule(*avals, **kwargs),
                            dtype_rule(*avals, **kwargs), weak_type=weak_type,
                            named_shape=named_shape_rule(*avals, **kwargs))
  elif least_specialized is core.DShapedArray:
    shape = shape_rule(*avals, **kwargs)
    ty = (core.ShapedArray if all(type(d) is int for d in shape)
          else core.DShapedArray)
    return ty(shape, dtype_rule(*avals, **kwargs), weak_type)
  elif least_specialized is core.UnshapedArray:
    return core.UnshapedArray(dtype_rule(*avals, **kwargs), weak_type=weak_type)
  else:
    raise TypeError(avals, least_specialized)
