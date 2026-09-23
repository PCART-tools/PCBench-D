def nextafter(x1: ArrayLike, x2: ArrayLike) -> Array:
  r"""Returns the next representable value after `x1` in the direction of `x2`.

  Note that in some environments flush-denormal-to-zero semantics is used.
  This means that, around zero, this function returns strictly non-zero
  values which appear as zero in any operations. Consider this example::

    >>> jnp.nextafter(0, 1)  # denormal numbers are representable
    Array(1.e-45, dtype=float32, weak_type=True)
    >>> jnp.nextafter(0, 1) * 1  # but are flushed to zero
    Array(0., dtype=float32, weak_type=True)

  For the smallest usable (i.e. normal) float, use ``tiny`` of ``jnp.finfo``.
  """
  return nextafter_p.bind(x1, x2)
