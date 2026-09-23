@_wraps(scipy.stats.rankdata, lax_description="""\
Currently the only supported nan_policy is 'propagate'
""")
@partial(jit, static_argnames=["method", "axis", "nan_policy"])
def rankdata(
  a: ArrayLike,
  method: str = "average",
  *,
  axis: Optional[int] = None,
  nan_policy: str = "propagate",
) -> Array:

  _check_arraylike("rankdata", a)

  if nan_policy not in ["propagate", "omit", "raise"]:
    raise ValueError(
      f"Illegal nan_policy value {nan_policy!r}; expected one of "
      "{'propoagate', 'omit', 'raise'}"
    )
  if nan_policy == "omit":
    raise NotImplementedError(
      f"Logic for `nan_policy` of {nan_policy} is not implemented"
    )
  if nan_policy == "raise":
    raise NotImplementedError(
      "In order to best JIT compile `mode`, we cannot know whether `x` "
      "contains nans. Please check if nans exist in `x` outside of the "
      "`rankdata` function."
    )

  if method not in ("average", "min", "max", "dense", "ordinal"):
    raise ValueError(f"unknown method '{method}'")

  a = jnp.asarray(a)

  if axis is not None:
    return jnp.apply_along_axis(rankdata, axis, a, method)

  arr = jnp.ravel(a)
  sorter = jnp.argsort(arr)
  inv = invert_permutation(sorter)

  if method == "ordinal":
    return inv + 1
  arr = arr[sorter]
  obs = jnp.insert(arr[1:] != arr[:-1], 0, True)
  dense = obs.cumsum()[inv]
  if method == "dense":
    return dense
  count = jnp.nonzero(obs, size=arr.size + 1, fill_value=len(obs))[0]
  if method == "max":
    return count[dense]
  if method == "min":
    return count[dense - 1] + 1
  if method == "average":
    return .5 * (count[dense] + count[dense - 1] + 1).astype(dtypes.canonicalize_dtype(jnp.float_))
  raise ValueError(f"unknown method '{method}'")
