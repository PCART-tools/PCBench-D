def _quantile(a: Array, q: Array, axis: Optional[Union[int, Tuple[int, ...]]],
              interpolation: str, keepdims: bool, squash_nans: bool) -> Array:
  if interpolation not in ["linear", "lower", "higher", "midpoint", "nearest"]:
    raise ValueError("interpolation can only be 'linear', 'lower', 'higher', "
                     "'midpoint', or 'nearest'")
  a, = util._promote_dtypes_inexact(a)
  keepdim = []
  if issubdtype(a.dtype, np.complexfloating):
    raise ValueError("quantile does not support complex input, as the operation is poorly defined.")
  if axis is None:
    a = ravel(a)
    axis = 0
  elif isinstance(axis, tuple):
    keepdim = list(shape(a))
    nd = ndim(a)
    axis = tuple(_canonicalize_axis(ax, nd) for ax in axis)
    if len(set(axis)) != len(axis):
      raise ValueError('repeated axis')
    for ax in axis:
      keepdim[ax] = 1

    keep = set(range(nd)) - set(axis)
    # prepare permutation
    dimensions = list(range(nd))
    for i, s in enumerate(sorted(keep)):
      dimensions[i], dimensions[s] = dimensions[s], dimensions[i]
    do_not_touch_shape = tuple(x for idx,x in enumerate(shape(a)) if idx not in axis)
    touch_shape = tuple(x for idx,x in enumerate(shape(a)) if idx in axis)
    a = lax.reshape(a, do_not_touch_shape + (int(np.prod(touch_shape)),), dimensions)
    axis = _canonicalize_axis(-1, ndim(a))
  else:
    axis = _canonicalize_axis(axis, ndim(a))

  q_shape = shape(q)
  q_ndim = ndim(q)
  if q_ndim > 1:
    raise ValueError(f"q must be have rank <= 1, got shape {shape(q)}")

  a_shape = shape(a)

  if squash_nans:
    a = where(ufuncs.isnan(a), nan, a) # Ensure nans are positive so they sort to the end.
    a = lax.sort(a, dimension=axis)
    counts = reductions.sum(ufuncs.logical_not(ufuncs.isnan(a)), axis=axis, dtype=q.dtype,
                            keepdims=keepdims)
    shape_after_reduction = counts.shape
    q = lax.expand_dims(
      q, tuple(range(q_ndim, len(shape_after_reduction) + q_ndim)))
    counts = lax.expand_dims(counts, tuple(range(q_ndim)))
    q = lax.mul(q, lax.sub(counts, _lax_const(q, 1)))
    low = lax.floor(q)
    high = lax.ceil(q)
    high_weight = lax.sub(q, low)
    low_weight = lax.sub(_lax_const(high_weight, 1), high_weight)

    low = lax.max(_lax_const(low, 0), lax.min(low, counts - 1))
    high = lax.max(_lax_const(high, 0), lax.min(high, counts - 1))
    low = lax.convert_element_type(low, int64)
    high = lax.convert_element_type(high, int64)
    out_shape = q_shape + shape_after_reduction
    index = [lax.broadcasted_iota(int64, out_shape, dim + q_ndim)
             for dim in range(len(shape_after_reduction))]
    if keepdims:
      index[axis] = low
    else:
      index.insert(axis, low)
    low_value = a[tuple(index)]
    index[axis] = high
    high_value = a[tuple(index)]
  else:
    a = where(reductions.any(ufuncs.isnan(a), axis=axis, keepdims=True), nan, a)
    a = lax.sort(a, dimension=axis)
    n = lax.convert_element_type(array(a_shape[axis]), lax_internal._dtype(q))
    q = lax.mul(q, n - 1)
    low = lax.floor(q)
    high = lax.ceil(q)
    high_weight = lax.sub(q, low)
    low_weight = lax.sub(_lax_const(high_weight, 1), high_weight)

    low = lax.clamp(_lax_const(low, 0), low, n - 1)
    high = lax.clamp(_lax_const(high, 0), high, n - 1)
    low = lax.convert_element_type(low, int64)
    high = lax.convert_element_type(high, int64)

    slice_sizes = list(a_shape)
    slice_sizes[axis] = 1
    dnums = lax.GatherDimensionNumbers(
      offset_dims=tuple(range(
        q_ndim,
        len(a_shape) + q_ndim if keepdims else len(a_shape) + q_ndim - 1)),
      collapsed_slice_dims=() if keepdims else (axis,),
      start_index_map=(axis,))
    low_value = lax.gather(a, low[..., None], dimension_numbers=dnums,
                           slice_sizes=slice_sizes)
    high_value = lax.gather(a, high[..., None], dimension_numbers=dnums,
                            slice_sizes=slice_sizes)
    if q_ndim == 1:
      low_weight = lax.broadcast_in_dim(low_weight, low_value.shape,
                                        broadcast_dimensions=(0,))
      high_weight = lax.broadcast_in_dim(high_weight, high_value.shape,
                                        broadcast_dimensions=(0,))

  if interpolation == "linear":
    result = lax.add(lax.mul(low_value.astype(q.dtype), low_weight),
                     lax.mul(high_value.astype(q.dtype), high_weight))
  elif interpolation == "lower":
    result = low_value
  elif interpolation == "higher":
    result = high_value
  elif interpolation == "nearest":
    pred = lax.le(high_weight, _lax_const(high_weight, 0.5))
    result = lax.select(pred, low_value, high_value)
  elif interpolation == "midpoint":
    result = lax.mul(lax.add(low_value, high_value), _lax_const(low_value, 0.5))
  else:
    raise ValueError(f"interpolation={interpolation!r} not recognized")
  if keepdims and keepdim:
    if q_ndim > 0:
      keepdim = [shape(q)[0], *keepdim]
    result = reshape(result,  keepdim)
  return lax.convert_element_type(result, a.dtype)
