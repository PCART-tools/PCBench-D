@util._wraps(np.where,
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
def where(condition: ArrayLike, x: Optional[ArrayLike] = None,
          y: Optional[ArrayLike] = None, *, size: Optional[int] = None,
          fill_value: Union[None, Array, Tuple[ArrayLike]] = None
    ) -> Union[Array, Tuple[Array, ...]]:
  if x is None and y is None:
    util.check_arraylike("where", condition)
    return nonzero(condition, size=size, fill_value=fill_value)
  else:
    util.check_arraylike("where", condition, x, y)
    if size is not None or fill_value is not None:
      raise ValueError("size and fill_value arguments cannot be used in three-term where function.")
    return util._where(condition, x, y)
