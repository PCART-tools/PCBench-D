@util._wraps(np.take_along_axis, update_doc=False,
        lax_description=TAKE_ALONG_AXIS_DOC)
@partial(jit, static_argnames=('axis', 'mode'))
def take_along_axis(arr, indices, axis: Optional[int],
                    mode: Optional[Union[str, lax.GatherScatterMode]] = None):
  util.check_arraylike("take_along_axis", arr, indices)
  index_dtype = dtypes.dtype(indices)
  if not dtypes.issubdtype(index_dtype, integer):
    raise TypeError("take_along_axis indices must be of integer type, got "
                    f"{str(index_dtype)}")
  if axis is None:
    if ndim(indices) != 1:
      msg = "take_along_axis indices must be 1D if axis=None, got shape {}"
      raise ValueError(msg.format(indices.shape))
    return take_along_axis(arr.ravel(), indices, 0)
  rank = ndim(arr)
  if rank != ndim(indices):
    msg = "indices and arr must have the same number of dimensions; {} vs. {}"
    raise ValueError(msg.format(ndim(indices), ndim(arr)))
  axis = _canonicalize_axis(axis, rank)

  def replace(tup, val):
    lst = list(tup)
    lst[axis] = val
    return tuple(lst)

  use_64bit_index = any([not core.is_constant_dim(d) or d >= (1 << 31) for d in arr.shape])
  index_dtype = dtype(int64 if use_64bit_index else int32)
  indices = lax.convert_element_type(indices, index_dtype)

  axis_size = arr.shape[axis]
  arr_shape = replace(arr.shape, 1)
  idx_shape = indices.shape
  out_shape = lax.broadcast_shapes(idx_shape, arr_shape)
  if axis_size == 0:
    return zeros(out_shape, arr.dtype)
  index_dims = [i for i, idx in enumerate(idx_shape) if i == axis or not core.definitely_equal(idx, 1)]

  gather_index_shape = tuple(np.array(out_shape)[index_dims]) + (1,)
  gather_indices = []
  slice_sizes = []
  offset_dims = []
  start_index_map = []
  collapsed_slice_dims = []
  j = 0
  for i in range(rank):
    if i == axis:
      indices = _normalize_index(indices, axis_size)
      gather_indices.append(lax.reshape(indices, gather_index_shape))
      slice_sizes.append(1)
      start_index_map.append(i)
      collapsed_slice_dims.append(i)
      j += 1
    elif core.definitely_equal(idx_shape[i], 1):
      # If idx_shape[i] == 1, we can just take the entirety of the arr's axis
      # and avoid forming an iota index.
      offset_dims.append(i)
      slice_sizes.append(arr_shape[i])
    elif core.definitely_equal(arr_shape[i], 1):
      # If the array dimension is 1 but the index dimension is not, we
      # broadcast the array dimension to the index dimension by repeatedly
      # gathering the first element.
      gather_indices.append(zeros(gather_index_shape, dtype=index_dtype))
      slice_sizes.append(1)
      start_index_map.append(i)
      collapsed_slice_dims.append(i)
      j += 1
    else:
      # Otherwise, idx_shape[i] == arr_shape[i]. Use an iota index so
      # corresponding elements of array and index are gathered.
      # TODO(mattjj): next line needs updating for dynamic shapes
      iota = lax.broadcasted_iota(index_dtype, gather_index_shape, j)
      gather_indices.append(iota)
      slice_sizes.append(1)
      start_index_map.append(i)
      collapsed_slice_dims.append(i)
      j += 1


  gather_indices_arr = lax.concatenate(gather_indices, dimension=j)
  dnums = lax.GatherDimensionNumbers(
    offset_dims=tuple(offset_dims),
    collapsed_slice_dims=tuple(collapsed_slice_dims),
    start_index_map=tuple(start_index_map))
  return lax.gather(arr, gather_indices_arr, dnums, tuple(slice_sizes),
                    mode="fill" if mode is None else mode)
