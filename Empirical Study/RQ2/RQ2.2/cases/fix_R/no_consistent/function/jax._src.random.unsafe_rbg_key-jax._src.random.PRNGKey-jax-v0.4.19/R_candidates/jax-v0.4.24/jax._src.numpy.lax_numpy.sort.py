@util.implements(np.sort, extra_params="""
kind : deprecated; specify sort algorithm using stable=True or stable=False
order : not supported
stable : bool, default=True
    Specify whether to use a stable sort.
descending : bool, default=False
    Specify whether to do a descending sort.
    """)
@partial(jit, static_argnames=('axis', 'kind', 'order', 'stable', 'descending'))
def sort(
    a: ArrayLike,
    axis: int | None = -1,
    kind: str | None = None,
    order: None = None, *,
    stable: bool = True,
    descending: bool = False,
) -> Array:
  util.check_arraylike("sort", a)
  if kind is not None:
    # Deprecated 2024-01-05
    warnings.warn("The 'kind' argument to sort has no effect, and is deprecated. "
                  "Use stable=True or stable=False to specify sort stability.",
                  category=DeprecationWarning, stacklevel=2)
  if order is not None:
    raise ValueError("'order' argument to sort is not supported.")
  if axis is None:
    arr = ravel(a)
    axis = 0
  else:
    arr = asarray(a)
  dimension = _canonicalize_axis(axis, arr.ndim)
  result = lax.sort(arr, dimension=dimension, is_stable=stable)
  return lax.rev(result, dimensions=[dimension]) if descending else result
