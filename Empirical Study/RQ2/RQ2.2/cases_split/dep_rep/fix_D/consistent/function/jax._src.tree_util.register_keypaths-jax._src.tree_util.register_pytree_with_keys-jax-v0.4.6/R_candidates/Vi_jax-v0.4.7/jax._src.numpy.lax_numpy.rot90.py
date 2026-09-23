@util._wraps(np.rot90, lax_description=_ARRAY_VIEW_DOC)
@partial(jit, static_argnames=('k', 'axes'))
def rot90(m: ArrayLike, k: int = 1, axes: Tuple[int, int] = (0, 1)) -> Array:
  util.check_arraylike("rot90", m)
  ax1, ax2 = axes
  ax1 = _canonicalize_axis(ax1, ndim(m))
  ax2 = _canonicalize_axis(ax2, ndim(m))
  if ax1 == ax2:
    raise ValueError("Axes must be different")  # same as numpy error
  k = k % 4
  if k == 0:
    return asarray(m)
  elif k == 2:
    return flip(flip(m, ax1), ax2)
  else:
    perm = list(range(ndim(m)))
    perm[ax1], perm[ax2] = perm[ax2], perm[ax1]
    if k == 1:
      return transpose(flip(m, ax2), perm)
    else:
      return flip(transpose(m, perm), ax2)
