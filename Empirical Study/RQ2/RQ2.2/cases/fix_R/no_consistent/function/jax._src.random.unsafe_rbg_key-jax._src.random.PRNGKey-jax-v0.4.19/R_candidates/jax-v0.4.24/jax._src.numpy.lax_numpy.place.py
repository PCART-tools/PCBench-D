@util.implements(np.place, lax_description="""
The semantics of :func:`numpy.place` is to modify arrays in-place, which JAX
cannot do because JAX arrays are immutable. Thus :func:`jax.numpy.place` adds
the ``inplace`` parameter, which must be set to ``False`` by the user as a
reminder of this API difference.
""", extra_params="""
inplace : bool, default=True
    If left to its default value of True, JAX will raise an error. This is because
    the semantics of :func:`numpy.put` are to modify the array in-place, which is
    not possible in JAX due to the immutability of JAX arrays.
""")
def place(arr: ArrayLike, mask: ArrayLike, vals: ArrayLike, *,
          inplace: bool = True) -> Array:
  util.check_arraylike("place", arr, mask, vals)
  data, mask_arr, vals_arr = asarray(arr), asarray(mask), ravel(vals)
  if inplace:
    raise ValueError(
      "jax.numpy.place cannot modify arrays in-place, because JAX arrays are immutable. "
      "Pass inplace=False to instead return an updated array.")
  if data.size != mask_arr.size:
    raise ValueError("place: arr and mask must be the same size")
  if not vals_arr.size:
    raise ValueError("Cannot place values from an empty array")
  if not data.size:
    return data
  indices = where(mask_arr.ravel(), size=mask_arr.size, fill_value=mask_arr.size)[0]
  vals_arr = _tile_to_size(vals_arr, len(indices))
  return data.ravel().at[indices].set(vals_arr, mode='drop').reshape(data.shape)
