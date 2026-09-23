@util.implements(np.argsort, extra_params="""
kind : deprecated; specify sort algorithm using stable=True or stable=False
order : not supported
stable : bool, default=True
    Specify whether to use a stable sort.
descending : bool, default=False
    Specify whether to do a descending sort.
    """)
@partial(jit, static_argnames=('axis', 'kind', 'order', 'stable', 'descending'))
def argsort(
    a: ArrayLike,
    axis: int | None = -1,
    kind: str | None = None,
    order: None = None,
    *, stable: bool = True,
    descending: bool = False,
) -> Array:
  util.check_arraylike("argsort", a)
  arr = asarray(a)
  if kind is not None:
    # Deprecated 2024-01-05
    warnings.warn("The 'kind' argument to argsort has no effect, and is deprecated. "
                  "Use stable=True or stable=False to specify sort stability.",
                  category=DeprecationWarning, stacklevel=2)
  if order is not None:
    raise ValueError("'order' argument to argsort is not supported.")
  if axis is None:
    arr = ravel(arr)
    axis = 0
  else:
    arr = asarray(a)
  dimension = _canonicalize_axis(axis, arr.ndim)
  use_64bit_index = not core.is_constant_dim(arr.shape[dimension]) or arr.shape[dimension] >= (1 << 31)
  iota = lax.broadcasted_iota(int64 if use_64bit_index else int_, arr.shape, dimension)
  # For stable descending sort, we reverse the array and indices to ensure that
  # duplicates remain in their original order when the final indices are reversed.
  # For non-stable descending sort, we can avoid these extra operations.
  if descending and stable:
    arr = lax.rev(arr, dimensions=[dimension])
    iota = lax.rev(iota, dimensions=[dimension])
  _, indices = lax.sort_key_val(arr, iota, dimension=dimension, is_stable=stable)
  return lax.rev(indices, dimensions=[dimension]) if descending else indices
