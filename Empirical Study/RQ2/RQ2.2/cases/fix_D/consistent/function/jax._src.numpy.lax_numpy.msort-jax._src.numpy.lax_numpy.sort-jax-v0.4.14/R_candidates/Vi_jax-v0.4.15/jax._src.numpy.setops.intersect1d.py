@_wraps(np.intersect1d)
def intersect1d(ar1: ArrayLike, ar2: ArrayLike, assume_unique: bool = False,
                return_indices: bool = False) -> Union[Array, tuple[Array, Array, Array]]:
  check_arraylike("intersect1d", ar1, ar2)
  ar1 = core.concrete_or_error(None, ar1, "The error arose in intersect1d()")
  ar2 = core.concrete_or_error(None, ar2, "The error arose in intersect1d()")

  if not assume_unique:
    if return_indices:
      ar1, ind1 = unique(ar1, return_index=True)
      ar2, ind2 = unique(ar2, return_index=True)
    else:
      ar1 = unique(ar1)
      ar2 = unique(ar2)
  else:
    ar1 = ravel(ar1)
    ar2 = ravel(ar2)

  if return_indices:
    aux, mask, aux_sort_indices = _intersect1d_sorted_mask(ar1, ar2, return_indices)
  else:
    aux, mask = _intersect1d_sorted_mask(ar1, ar2, return_indices)

  int1d = aux[:-1][mask]

  if return_indices:
    ar1_indices = aux_sort_indices[:-1][mask]
    ar2_indices = aux_sort_indices[1:][mask] - np.size(ar1)
    if not assume_unique:
      ar1_indices = ind1[ar1_indices]
      ar2_indices = ind2[ar2_indices]

    return int1d, ar1_indices, ar2_indices
  else:
    return int1d
