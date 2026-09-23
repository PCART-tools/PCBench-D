def _pile_flatten(pile):
  lengths = []
  new_shape = [lengths.append(d.lengths) or d.replace(lengths=len(lengths))
               if type(d) is IndexedAxisSize else d
               for d in pile.aval.elt_ty.shape]
  elt_ty = pile.aval.elt_ty.update(shape=tuple(new_shape))
  aval = pile.aval.replace(elt_ty=elt_ty)
  return (lengths, pile.data), aval
