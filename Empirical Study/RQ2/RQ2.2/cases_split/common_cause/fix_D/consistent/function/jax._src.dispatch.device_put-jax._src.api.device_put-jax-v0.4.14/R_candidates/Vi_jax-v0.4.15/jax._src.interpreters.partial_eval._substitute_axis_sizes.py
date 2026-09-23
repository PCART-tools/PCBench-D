def _substitute_axis_sizes(env: dict, aval: AbstractValue) -> AbstractValue:
  if isinstance(aval, DShapedArray):
    shp = []
    for d in aval.shape:
      if isinstance(d, core.DArray):
        assert not d.shape and type(d.dtype) is core.bint
        shp.append(BoundedAxisSize(int(d._data), int(d.dtype.bound)))
      elif (type(d) is core.Var and isinstance(d.aval, core.DShapedArray) and
            type(d.aval.dtype) is core.bint):
        assert not d.aval.shape
        shp.append(BoundedAxisSize(env[d], d.aval.dtype.bound))
      else:
        shp.append(env.get(d, d))
    return DShapedArray(tuple(shp), aval.dtype, aval.weak_type)
  else:
    return aval
