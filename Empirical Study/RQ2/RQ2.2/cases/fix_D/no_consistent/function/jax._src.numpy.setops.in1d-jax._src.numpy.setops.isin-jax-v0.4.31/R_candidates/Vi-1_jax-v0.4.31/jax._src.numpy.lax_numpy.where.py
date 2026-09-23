def where(condition, x=None, y=None, /, *, size=None, fill_value=None):
  """Select elements from two arrays based on a condition.

  JAX implementation of :func:`numpy.where`.

  .. note::
     when only ``condition`` is provided, ``jnp.where(condition)`` is equivalent
     to ``jnp.nonzero(condition)``. For that case, refer to the documentation of
     :func:`jax.numpy.nonzero`. The docstring below focuses on the case where
     ``x`` and ``y`` are specified.

  The three-term version of ``jnp.where`` lowers to :func:`jax.lax.select`.

  Args:
    condition: boolean array. Must be broadcast-compatible with ``x`` and ``y`` when
      they are specified.
    x: arraylike. Should be broadcast-compatible with ``condition`` and ``y``, and
      typecast-compatible with ``y``.
    y: arraylike. Should be broadcast-compatible with ``condition`` and ``x``, and
      typecast-compatible with ``x``.
    size: integer, only referenced when ``x`` and ``y`` are ``None``. For details,
      see :func:`jax.numpy.nonzero`.
    fill_value: only referenced when ``x`` and ``y`` are ``None``. For details,
      see :func:`jax.numpy.nonzero`.

  Returns:
    An array of dtype ``jnp.result_type(x, y)`` with values drawn from ``x`` where ``condition``
    is True, and from ``y`` where condition is ``False. If ``x`` and ``y`` are ``None``, the
    function behaves differently; see `:func:`jax.numpy.nonzero` for a description of the return
    type.

  See Also:
    - :func:`jax.numpy.nonzero`
    - :func:`jax.numpy.argwhere`
    - :func:`jax.lax.select`

  Notes:
    Special care is needed when the ``x`` or ``y`` input to :func:`jax.numpy.where` could
    have a value of NaN. Specifically, when a gradient is taken with :func:`jax.grad`
    (reverse-mode differentiation), a NaN in either ``x`` or ``y`` will propagate into the
    gradient, regardless of the value of ``condition``.  More information on this behavior
    and workarounds is available in the `JAX FAQ
    <https://jax.readthedocs.io/en/latest/faq.html#gradients-contain-nan-where-using-where>`_.

  Examples:
    When ``x`` and ``y`` are not provided, ``where`` behaves equivalently to
    :func:`jax.numpy.nonzero`:

    >>> x = jnp.arange(10)
    >>> jnp.where(x > 4)
    (Array([5, 6, 7, 8, 9], dtype=int32),)
    >>> jnp.nonzero(x > 4)
    (Array([5, 6, 7, 8, 9], dtype=int32),)

    When ``x`` and ``y`` are provided, ``where`` selects between them based on
    the specified condition:

    >>> jnp.where(x > 4, x, 0)
    Array([0, 0, 0, 0, 0, 5, 6, 7, 8, 9], dtype=int32)
  """
  if x is None and y is None:
    util.check_arraylike("where", condition)
    return nonzero(condition, size=size, fill_value=fill_value)
  else:
    util.check_arraylike("where", condition, x, y)
    if size is not None or fill_value is not None:
      raise ValueError("size and fill_value arguments cannot be used in "
                       "three-term where function.")
    if x is None or y is None:
      raise ValueError("Either both or neither of the x and y arguments "
                       "should be provided to jax.numpy.where, got "
                       f"{x} and {y}.")
    return util._where(condition, x, y)
