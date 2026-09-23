def matchaxis(axis_name, sz, src, dst, x, sum_match=False):
  if dst == pile_axis:
    x = bdim_at_front(x, src, sz)
    elt_ty = x.aval.update(shape=x.shape[1:])
    aval = PileTy(core.Var(0, '', core.ShapedArray((), np.dtype('int32'))),
                  x.shape[0], elt_ty)
    return Pile(aval, x)
  try:
    _ = core.get_aval(x)
  except TypeError as e:
    raise TypeError(f"Output from batched function {repr(x)} with type "
                    f"{type(x)} is not a valid JAX type") from e
  if src == dst:
    return x
  elif type(src) == type(dst) == int:
    return moveaxis(x, src, dst)
  elif src is not_mapped and dst is not not_mapped:
    return broadcast(x, sz, canonicalize_axis(dst, np.ndim(x) + 1))
  elif dst is not_mapped and sum_match:
    return x.sum(src)
  else:
    if (not isinstance(axis_name, core._TempAxisName) and
        axis_name is not core.no_axis_name):
      raise ValueError(f'vmap has mapped output ({axis_name=}) but out_axes is {dst}')
    else:
      raise ValueError(f'vmap has mapped output but out_axes is {dst}')
