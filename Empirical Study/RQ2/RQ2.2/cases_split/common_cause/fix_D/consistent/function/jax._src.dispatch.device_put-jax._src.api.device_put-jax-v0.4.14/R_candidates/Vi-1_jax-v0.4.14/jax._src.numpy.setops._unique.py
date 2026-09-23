def _unique(ar: Array, axis: int, return_index: bool = False, return_inverse: bool = False,
            return_counts: bool = False, size: Optional[int] = None,
            fill_value: Optional[ArrayLike] = None, return_true_size: bool = False
            ) -> Union[Array, tuple[Array, ...]]:
  """
  Find the unique elements of an array along a particular axis.
  """
  if ar.shape[axis] == 0 and size and fill_value is None:
    raise ValueError(
      "jnp.unique: for zero-sized input with nonzero size argument, fill_value must be specified")

  aux, mask, perm = _unique_sorted_mask(ar, axis)
  if size is None:
    ind = core.concrete_or_error(None, mask,
        "The error arose in jnp.unique(). " + UNIQUE_SIZE_HINT)
  else:
    ind = nonzero(mask, size=size)[0]
  result = aux[ind] if aux.size else aux
  if fill_value is not None:
    fill_value = asarray(fill_value, dtype=result.dtype)
  if size is not None and fill_value is not None:
    if result.shape[0]:
      valid = lax.expand_dims(arange(size) < mask.sum(), tuple(range(1, result.ndim)))
      result = where(valid, result, fill_value)
    else:
      result = full_like(result, fill_value, shape=(size, *result.shape[1:]))
  result = moveaxis(result, 0, axis)

  ret: tuple[Array, ...] = (result,)
  if return_index:
    if aux.size:
      ret += (perm[ind],)
    else:
      ret += (perm,)
  if return_inverse:
    if aux.size:
      imask = cumsum(mask) - 1
      inv_idx = zeros(mask.shape, dtype=dtypes.canonicalize_dtype(dtypes.int_))
      inv_idx = inv_idx.at[perm].set(imask)
    else:
      inv_idx = zeros(ar.shape[axis], dtype=int)
    ret += (inv_idx,)
  if return_counts:
    if aux.size:
      if size is None:
        idx = append(nonzero(mask)[0], mask.size)
      else:
        idx = nonzero(mask, size=size + 1)[0]
        idx = idx.at[1:].set(where(idx[1:], idx[1:], mask.size))
      ret += (diff(idx),)
    elif ar.shape[axis]:
      ret += (array([ar.shape[axis]], dtype=dtypes.canonicalize_dtype(dtypes.int_)),)
    else:
      ret += (empty(0, dtype=int),)
  if return_true_size:
    # Useful for internal uses of unique().
    ret += (mask.sum(),)
  return ret[0] if len(ret) == 1 else ret
