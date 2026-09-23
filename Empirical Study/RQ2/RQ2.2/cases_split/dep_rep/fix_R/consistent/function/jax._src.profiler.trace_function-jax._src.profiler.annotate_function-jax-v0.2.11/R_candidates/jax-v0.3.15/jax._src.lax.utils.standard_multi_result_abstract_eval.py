def standard_multi_result_abstract_eval(
    prim, shape_rule, dtype_rule, weak_type_rule,
    named_shape_rule, *avals, **kwargs):
  assert prim.multiple_results
  assert all(isinstance(aval, core.UnshapedArray) for aval in avals), avals
  least_specialized = _max(map(type, avals),
                           key=operator.attrgetter('array_abstraction_level'))
  weak_types = weak_type_rule(*avals, **kwargs)
  if least_specialized is core.ConcreteArray:
    out_vals = prim.impl(*[x.val for x in avals], **kwargs)
    return [core.ConcreteArray(val.dtype, val, weak_type=weak_type)
            for val, weak_type in safe_zip(out_vals, weak_types)]
  elif least_specialized is core.ShapedArray:
    out_shapes = shape_rule(*avals, **kwargs)
    out_dtypes = dtype_rule(*avals, **kwargs)
    out_named_shapes = named_shape_rule(*avals, **kwargs)
    return [core.ShapedArray(s, d, weak_type=weak_type, named_shape=named_shape)
            for s, d, weak_type, named_shape
            in safe_zip(out_shapes, out_dtypes, weak_types, out_named_shapes)]
  elif least_specialized is core.UnshapedArray:
    out_dtypes = dtype_rule(*avals, **kwargs)
    return [core.UnshapedArray(dtype, weak_type=weak_type)
            for dtype, weak_type in safe_zip(out_dtypes, weak_types)]
  else:
    raise TypeError(avals, least_specialized)
