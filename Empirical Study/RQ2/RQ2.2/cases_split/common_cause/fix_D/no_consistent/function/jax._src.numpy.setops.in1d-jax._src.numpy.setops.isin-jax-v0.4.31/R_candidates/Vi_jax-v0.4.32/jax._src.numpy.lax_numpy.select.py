def select(
    condlist: Sequence[ArrayLike],
    choicelist: Sequence[ArrayLike],
    default: ArrayLike = 0,
) -> Array:
  """Select values based on a series of conditions.

  JAX implementation of :func:`numpy.select`, implemented in terms
  of :func:`jax.lax.select_n`

  Args:
    condlist: sequence of array-like conditions. All entries must be mutually
      broadcast-compatible.
    choicelist: sequence of array-like values to choose. Must have the same length
      as ``condlist``, and all entries must be broadcast-compatible with entries
      of ``condlist``.
    default: value to return when every condition is False (default: 0).

  Returns:
    Array of selected values from ``choicelist`` corresponding to the first
    ``True`` entry in ``condlist`` at each location.

  See also:
    - :func:`jax.numpy.where`: select between two values based on a single condition.
    - :func:`jax.lax.select_n`: select between *N* values based on an index.

  Examples:
    >>> condlist = [
    ...    jnp.array([False, True, False, False]),
    ...    jnp.array([True, False, False, False]),
    ...    jnp.array([False, True, True, False]),
    ... ]
    >>> choicelist = [
    ...    jnp.array([1, 2, 3, 4]),
    ...    jnp.array([10, 20, 30, 40]),
    ...    jnp.array([100, 200, 300, 400]),
    ... ]
    >>> jnp.select(condlist, choicelist, default=0)
    Array([ 10,   2, 300,   0], dtype=int32)

    This is logically equivalent to the following nested ``where`` statement:

    >>> default = 0
    >>> jnp.where(condlist[0],
    ...   choicelist[0],
    ...   jnp.where(condlist[1],
    ...     choicelist[1],
    ...     jnp.where(condlist[2],
    ...       choicelist[2],
    ...       default)))
    Array([ 10,   2, 300,   0], dtype=int32)

    However, for efficiency it is implemented in terms of :func:`jax.lax.select_n`.
  """
  if len(condlist) != len(choicelist):
    msg = "condlist must have length equal to choicelist ({} vs {})"
    raise ValueError(msg.format(len(condlist), len(choicelist)))
  if len(condlist) == 0:
    raise ValueError("condlist must be non-empty")
  # Put the default at front with condition False because
  # argmax returns zero for an array of False values.
  choicelist = util.promote_dtypes(default, *choicelist)
  conditions = stack(broadcast_arrays(False, *condlist))
  idx = argmax(conditions.astype(bool), axis=0)
  return lax.select_n(*broadcast_arrays(idx, *choicelist))
