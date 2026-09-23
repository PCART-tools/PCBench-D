@partial(jit, static_argnames=('k', 'axes'))
def rot90(m: ArrayLike, k: int = 1, axes: tuple[int, int] = (0, 1)) -> Array:
  """Rotate an array by 90 degrees counterclockwise in the plane specified by axes.

  JAX implementation of :func:`numpy.rot90`.

  Args:
    m: input array. Must have ``m.ndim >= 2``.
    k: int, optional, default=1. Specifies the number of times the array is rotated.
      For negative values of ``k``, the array is rotated in clockwise direction.
    axes: tuple of 2 integers, optional, default= (0, 1). The axes define the plane
      in which the array is rotated. Both the axes must be different.

  Returns:
    An array containing the copy of the input, ``m`` rotated by 90 degrees.

  See also:
    - :func:`jax.numpy.flip`: reverse the order along the given axis
    - :func:`jax.numpy.fliplr`: reverse the order along axis 1 (left/right)
    - :func:`jax.numpy.flipud`: reverse the order along axis 0 (up/down)

  Examples:
    >>> m = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.rot90(m)
    Array([[3, 6],
           [2, 5],
           [1, 4]], dtype=int32)
    >>> jnp.rot90(m, k=2)
    Array([[6, 5, 4],
           [3, 2, 1]], dtype=int32)

    ``jnp.rot90(m, k=1, axes=(1, 0))`` is equivalent to
    ``jnp.rot90(m, k=-1, axes(0,1))``.

    >>> jnp.rot90(m, axes=(1, 0))
    Array([[4, 1],
           [5, 2],
           [6, 3]], dtype=int32)
    >>> jnp.rot90(m, k=-1, axes=(0, 1))
    Array([[4, 1],
           [5, 2],
           [6, 3]], dtype=int32)

    when input array has ``ndim>2``:

    >>> m1 = jnp.array([[[1, 2, 3],
    ...                  [4, 5, 6]],
    ...                 [[7, 8, 9],
    ...                  [10, 11, 12]]])
    >>> jnp.rot90(m1, k=1, axes=(2, 1))
    Array([[[ 4,  1],
            [ 5,  2],
            [ 6,  3]],
    <BLANKLINE>
           [[10,  7],
            [11,  8],
            [12,  9]]], dtype=int32)
  """
  util.check_arraylike("rot90", m)
  if np.ndim(m) < 2:
    raise ValueError("rot90 requires its first argument to have ndim at least "
                     f"two, but got first argument of shape {np.shape(m)}, "
                     f"which has ndim {np.ndim(m)}")
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
