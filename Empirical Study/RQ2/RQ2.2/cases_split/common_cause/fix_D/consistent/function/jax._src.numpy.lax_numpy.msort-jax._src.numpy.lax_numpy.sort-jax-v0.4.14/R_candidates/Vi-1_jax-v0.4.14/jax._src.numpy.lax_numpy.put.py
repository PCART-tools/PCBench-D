@util._wraps(np.put, lax_description="""
The semantics of :func:`numpy.put` is to modify arrays in-place, which JAX
cannot do because JAX arrays are immutable. Thus :func:`jax.numpy.put` adds
the ``inplace`` parameter, which must be set to ``False`` by the user as a
reminder of this API difference.
""", extra_params="""
inplace : bool, default=True
    If left to its default value of True, JAX will raise an error. This is because
    the semantics of :func:`numpy.put` are to modify the array in-place, which is
    not possible in JAX due to the immutability of JAX arrays.
""")
def put(a: ArrayLike, ind: ArrayLike, v: ArrayLike,
        mode: str | None = None, *, inplace: bool = True) -> Array:
  util.check_arraylike("put", a, ind, v)
  arr, ind_arr, v_arr = asarray(a), ravel(ind), ravel(v)
  if not arr.size or not ind_arr.size or not v_arr.size:
    return arr
  v_arr = tile(v_arr, int(np.ceil(len(ind_arr) / len(v_arr))))[:len(ind_arr)]
  if inplace:
    raise ValueError(
      "jax.numpy.put cannot modify arrays in-place, because JAX arrays are immutable. "
      "Pass inplace=False to instead return an updated array.")
  if mode is None:
    scatter_mode = "drop"
  elif mode == "clip":
    ind_arr = clip(ind_arr, 0, arr.size - 1)
    scatter_mode = "promise_in_bounds"
  elif mode == "wrap":
    ind_arr = ind_arr % arr.size
    scatter_mode = "promise_in_bounds"
  elif mode == "raise":
    raise NotImplementedError("The 'raise' mode to jnp.put is not supported.")
  else:
    raise ValueError(f"mode should be one of 'wrap' or 'clip'; got {mode=}")
  return arr.at[unravel_index(ind_arr, arr.shape)].set(v_arr, mode=scatter_mode)
