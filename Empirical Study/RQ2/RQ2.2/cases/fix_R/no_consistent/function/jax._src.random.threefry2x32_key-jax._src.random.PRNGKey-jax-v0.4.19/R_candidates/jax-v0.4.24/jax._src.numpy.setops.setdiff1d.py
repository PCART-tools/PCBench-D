@implements(np.setdiff1d,
  lax_description=_dedent("""
    Because the size of the output of ``setdiff1d`` is data-dependent, the function is not
    typically compatible with JIT. The JAX version adds the optional ``size`` argument which
    must be specified statically for ``jnp.setdiff1d`` to be used within some of JAX's
    transformations."""),
  extra_params=_dedent("""
    size : int, optional
        If specified, the first ``size`` elements of the result will be returned. If there are
        fewer elements than ``size`` indicates, the return value will be padded with ``fill_value``.
    fill_value : array_like, optional
        When ``size`` is specified and there are fewer than the indicated number of elements, the
        remaining elements will be filled with ``fill_value``, which defaults to zero."""))
def setdiff1d(ar1: ArrayLike, ar2: ArrayLike, assume_unique: bool = False,
              *, size: int | None = None, fill_value: ArrayLike | None = None) -> Array:
  check_arraylike("setdiff1d", ar1, ar2)
  if size is None:
    ar1 = core.concrete_or_error(None, ar1, "The error arose in setdiff1d()")
  else:
    size = core.concrete_or_error(operator.index, size, "The error arose in setdiff1d()")
  arr1 = asarray(ar1)
  fill_value = asarray(0 if fill_value is None else fill_value, dtype=arr1.dtype)
  if arr1.size == 0:
    return full_like(arr1, fill_value, shape=size or 0)
  if not assume_unique:
    arr1 = cast(Array, unique(arr1, size=size and arr1.size))
  mask = _in1d(arr1, ar2, invert=True)
  if size is None:
    return arr1[mask]
  else:
    if not (assume_unique or size is None):
      # Set mask to zero at locations corresponding to unique() padding.
      n_unique = arr1.size + 1 - (arr1 == arr1[0]).sum()
      mask = where(arange(arr1.size) < n_unique, mask, False)
    return where(arange(size) < mask.sum(), arr1[where(mask, size=size)], fill_value)
