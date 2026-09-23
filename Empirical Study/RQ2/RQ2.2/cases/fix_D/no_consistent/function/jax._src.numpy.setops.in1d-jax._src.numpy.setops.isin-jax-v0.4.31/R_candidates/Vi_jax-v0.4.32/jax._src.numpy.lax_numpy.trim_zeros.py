def trim_zeros(filt, trim='fb'):
  """Trim leading and/or trailing zeros of the input array.

  JAX implementation of :func:`numpy.trim_zeros`.

  Args:
    filt: input array. Must have ``filt.ndim == 1``.
    trim: string, optional, default = ``fb``. Specifies from which end the input
      is trimmed.

      - ``f`` - trims only the leading zeros.
      - ``b`` - trims only the trailing zeros.
      - ``fb`` - trims both leading and trailing zeros.

  Returns:
    An array containig the trimmed input with same dtype as ``filt``.

  Examples:
    >>> x = jnp.array([0, 0, 2, 0, 1, 4, 3, 0, 0, 0])
    >>> jnp.trim_zeros(x)
    Array([2, 0, 1, 4, 3], dtype=int32)
  """
  filt = core.concrete_or_error(asarray, filt,
    "Error arose in the `filt` argument of trim_zeros()")
  nz = (filt == 0)
  if reductions.all(nz):
    return empty(0, _dtype(filt))
  start = argmin(nz) if 'f' in trim.lower() else 0
  end = argmin(nz[::-1]) if 'b' in trim.lower() else 0
  return filt[start:len(filt) - end]
