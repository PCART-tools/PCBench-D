def _jumble_flatten(jumble):
  lengths = []
  new_shape = [lengths.append(d.lengths) or d.replace(lengths=len(lengths))
               if type(d) is IndexedAxisSize else d
               for d in jumble.aval.elt_ty.shape]
  elt_ty = jumble.aval.elt_ty.update(shape=tuple(new_shape))
  aval = jumble.aval.replace(elt_ty=elt_ty)
  return (lengths, jumble.data), aval
