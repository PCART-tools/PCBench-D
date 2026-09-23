@util.implements(np.where,  # type: ignore[no-redef]
  lax_description=_dedent("""
    At present, JAX does not support JIT-compilation of the single-argument form
    of :py:func:`jax.numpy.where` because its output shape is data-dependent. The
    three-argument form does not have a data-dependent shape and can be JIT-compiled
    successfully. Alternatively, you can use the optional ``size`` keyword to
    statically specify the expected size of the output.\n\n

    Special care is needed when the ``x`` or ``y`` input to
    :py:func:`jax.numpy.where` could have a value of NaN.
    Specifically, when a gradient is taken
    with :py:func:`jax.grad` (reverse-mode differentiation), a NaN in either
    ``x`` or ``y`` will propagate into the gradient, regardless of the value
    of ``condition``.  More information on this behavior and workarounds
    is available in the JAX FAQ:
    https://jax.readthedocs.io/en/latest/faq.html#gradients-contain-nan-where-using-where"""),
  extra_params=_dedent("""
    size : int, optional
        Only referenced when ``x`` and ``y`` are ``None``. If specified, the indices of the first
        ``size`` elements of the result will be returned. If there are fewer elements than ``size``
        indicates, the return value will be padded with ``fill_value``.
    fill_value : array_like, optional
        When ``size`` is specified and there are fewer than the indicated number of elements, the
        remaining elements will be filled with ``fill_value``, which defaults to zero."""))
def where(
    acondition = None, if_true = None, if_false = None, /, *,
    size=None, fill_value=None,
    # Deprecated keyword-only names.
    condition = _DEPRECATED_WHERE_ARG, x = _DEPRECATED_WHERE_ARG,
    y = _DEPRECATED_WHERE_ARG
) -> Array | tuple[Array, ...]:
  if (condition is not _DEPRECATED_WHERE_ARG or x is not _DEPRECATED_WHERE_ARG
      or y is not _DEPRECATED_WHERE_ARG):
    # TODO(phawkins): deprecated Nov 17 2023, remove after deprecation expires.
    warnings.warn(
        "Passing condition, x, or y to jax.numpy.where via keyword arguments "
        "is deprecated.",
        DeprecationWarning,
        stacklevel=2,
    )
  if condition is not _DEPRECATED_WHERE_ARG:
    if acondition is not None:
      raise ValueError("condition should be a positional-only argument")
    acondition = condition
  if x is not _DEPRECATED_WHERE_ARG:
    if if_true is not None:
      raise ValueError("x should be a positional-only argument")
    if_true = x
  if y is not _DEPRECATED_WHERE_ARG:
    if if_false is not None:
      raise ValueError("y should be a positional-only argument")
    if_false = y

  if if_true is None and if_false is None:
    util.check_arraylike("where", acondition)
    return nonzero(acondition, size=size, fill_value=fill_value)
  else:
    util.check_arraylike("where", acondition, if_true, if_false)
    if size is not None or fill_value is not None:
      raise ValueError("size and fill_value arguments cannot be used in three-term where function.")
    return util._where(acondition, if_true, if_false)
