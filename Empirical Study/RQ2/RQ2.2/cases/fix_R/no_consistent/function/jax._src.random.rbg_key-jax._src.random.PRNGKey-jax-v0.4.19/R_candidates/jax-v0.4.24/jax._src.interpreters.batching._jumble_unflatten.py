def _jumble_unflatten(aval, x):
  lengths, data = x
  new_shape = [d.replace(lengths=lengths[d.lengths - 1])
               if type(d) is IndexedAxisSize else d
               for d in aval.elt_ty.shape]
  elt_ty = aval.elt_ty.update(shape=tuple(new_shape))
  aval = aval.replace(elt_ty=elt_ty)
  return Jumble(aval, data)
