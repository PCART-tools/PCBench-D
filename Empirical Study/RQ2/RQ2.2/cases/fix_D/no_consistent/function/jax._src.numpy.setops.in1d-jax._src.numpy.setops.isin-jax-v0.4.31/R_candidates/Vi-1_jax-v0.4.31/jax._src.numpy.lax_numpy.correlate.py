@partial(jit, static_argnames=('mode', 'precision', 'preferred_element_type'))
def correlate(a: ArrayLike, v: ArrayLike, mode: str = 'valid', *,
              precision: PrecisionLike = None,
              preferred_element_type: DTypeLike | None = None) -> Array:
  r"""Correlation of two one dimensional arrays.

  JAX implementation of :func:`numpy.correlate`.

  Correlation of one dimensional arrays is defined as:

  .. math::

     c_k = \sum_j a_{k + j} \overline{v_j}

  where :math:`\overline{v_j}` is the complex conjugate of :math:`v_j`.

  Args:
    a: left-hand input to the correlation. Must have ``a.ndim == 1``.
    v: right-hand input to the correlation. Must have ``v.ndim == 1``.
    mode: controls the size of the output. Available operations are:

      * ``"full"``: output the full correlation of the inputs.
      * ``"same"``: return a centered portion of the ``"full"`` output which
        is the same size as ``a``.
      * ``"valid"``: (default) return the portion of the ``"full"`` output which do not
        depend on padding at the array edges.

    precision: Specify the precision of the computation. Refer to
      :class:`jax.lax.Precision` for a description of available values.

    preferred_element_type: A datatype, indicating to accumulate results to and
      return a result with that datatype. Default is ``None``, which means the
      default accumulation type for the input types.

  Returns:
    Array containing the cross-correlation result.

  See Also:
    - :func:`jax.scipy.signal.correlate`: ND correlation
    - :func:`jax.numpy.convolve`: 1D convolution

  Examples:
    >>> x = jnp.array([1, 2, 3, 2, 1])
    >>> y = jnp.array([4, 5, 6])

    Since default ``mode = 'valid'``, ``jax.numpy.correlate`` returns only the
    portion of correlation where the two arrays fully overlap:

    >>> jnp.correlate(x, y)
    Array([32., 35., 28.], dtype=float32)

    Specifying ``mode = 'full'`` returns full correlation using implicit
    zero-padding at the edges.

    >>> jnp.correlate(x, y, mode='full')
    Array([ 6., 17., 32., 35., 28., 13.,  4.], dtype=float32)

    Specifying ``mode = 'same'`` returns a centered correlation the same size
    as the first input:

    >>> jnp.correlate(x, y, mode='same')
    Array([17., 32., 35., 28., 13.], dtype=float32)

    If both the inputs arrays are real-valued and symmetric then the result will
    also be symmetric and will be equal to the result of ``jax.numpy.convolve``.

    >>> x1 = jnp.array([1, 2, 3, 2, 1])
    >>> y1 = jnp.array([4, 5, 4])
    >>> jnp.correlate(x1, y1, mode='full')
    Array([ 4., 13., 26., 31., 26., 13.,  4.], dtype=float32)
    >>> jnp.convolve(x1, y1, mode='full')
    Array([ 4., 13., 26., 31., 26., 13.,  4.], dtype=float32)

    For complex-valued inputs:

    >>> x2 = jnp.array([3+1j, 2, 2-3j])
    >>> y2 = jnp.array([4, 2-5j, 1])
    >>> jnp.correlate(x2, y2, mode='full')
    Array([ 3. +1.j,  3.+17.j, 18.+11.j, 27. +4.j,  8.-12.j], dtype=complex64)
  """
  util.check_arraylike("correlate", a, v)
  return _conv(asarray(a), asarray(v), mode=mode, op='correlate',
               precision=precision, preferred_element_type=preferred_element_type)
