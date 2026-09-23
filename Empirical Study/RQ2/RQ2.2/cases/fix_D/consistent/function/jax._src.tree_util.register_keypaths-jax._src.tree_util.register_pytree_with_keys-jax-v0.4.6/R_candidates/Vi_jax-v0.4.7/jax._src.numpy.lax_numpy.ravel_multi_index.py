@util._wraps(np.ravel_multi_index)
def ravel_multi_index(multi_index: Tuple[ArrayLike, ...], dims: Tuple[int, ...],
                      mode: str = 'raise', order: str = 'C') -> Array:
  assert len(multi_index) == len(dims), f"len(multi_index)={len(multi_index)} != len(dims)={len(dims)}"
  dims = tuple(core.concrete_or_error(operator.index, d, "in `dims` argument of ravel_multi_index().") for d in dims)
  util.check_arraylike("ravel_multi_index", *multi_index)
  multi_index_arr = [asarray(i) for i in multi_index]
  for index in multi_index_arr:
    if mode == 'raise':
      core.concrete_or_error(array, index,
        "The error occurred because ravel_multi_index was jit-compiled"
        " with mode='raise'. Use mode='wrap' or mode='clip' instead.")
    if not issubdtype(_dtype(index), integer):
      raise TypeError("only int indices permitted")
  if mode == "raise":
    if _any(reductions.any((i < 0) | (i >= d)) for i, d in zip(multi_index_arr, dims)):
      raise ValueError("invalid entry in coordinates array")
  elif mode == "clip":
    multi_index_arr = [clip(i, 0, d - 1) for i, d in zip(multi_index_arr, dims)]
  elif mode == "wrap":
    multi_index_arr = [i % d for i, d in zip(multi_index_arr, dims)]
  else:
    raise ValueError(f"invalid mode={mode!r}. Expected 'raise', 'wrap', or 'clip'")

  if order == "F":
    strides = np.cumprod((1,) + dims[:-1])
  elif order == "C":
    strides = np.cumprod((1,) + dims[1:][::-1])[::-1]
  else:
    raise ValueError(f"invalid order={order!r}. Expected 'C' or 'F'")

  result = array(0, dtype=(multi_index_arr[0].dtype if multi_index_arr
                           else dtypes.canonicalize_dtype(int_)))
  for i, s in zip(multi_index_arr, strides):
    result = result + i * int(s)
  return result
