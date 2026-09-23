@partial(jit, static_argnames=('mode', 'precision', 'preferred_element_type'))
def convolve(a: ArrayLike, v: ArrayLike, mode: str = 'full', *,
             precision: PrecisionLike = None,
             preferred_element_type: DTypeLike | None = None) -> Array:
  r"""Convolution of two one dimensional arrays.

  JAX implementation of :func:`numpy.convolve`.

  Convolution of one dimensional arrays is defined as:

  .. math::

     c_k = \sum_j a_{k - j} v_j

  Args:
    a: left-hand input to the convolution. Must have ``a.ndim == 1``.
    v: right-hand input to the convolution. Must have ``v.ndim == 1``.
    mode: controls the size of the output. Available operations are:

      * ``"full"``: (default) output the full convolution of the inputs.
      * ``"same"``: return a centered portion of the ``"full"`` output which
        is the same size as ``a``.
      * ``"valid"``: return the portion of the ``"full"`` output which do not
        depend on padding at the array edges.

    precision: Specify the precision of the computation. Refer to
      :class:`jax.lax.Precision` for a description of available values.

    preferred_element_type: A datatype, indicating to accumulate results to and
      return a result with that datatype. Default is ``None``, which means the
      default accumulation type for the input types.

  Returns:
    Array containing the convolved result.

  See Also:
    - :func:`jax.scipy.signal.convolve`: ND convolution
    - :func:`jax.numpy.correlate`: 1D correlation

  Examples:
    A few 1D convolution examples:

    >>> x = jnp.array([1, 2, 3, 2, 1])
    >>> y = jnp.array([4, 1, 2])

    ``jax.numpy.convolve``, by default, returns full convolution using implicit
    zero-padding at the edges:

    >>> jnp.convolve(x, y)
    Array([ 4.,  9., 16., 15., 12.,  5.,  2.], dtype=float32)

    Specifying ``mode = 'same'`` returns a centered convolution the same size
    as the first input:

    >>> jnp.convolve(x, y, mode='same')
    Array([ 9., 16., 15., 12.,  5.], dtype=float32)

    Specifying ``mode = 'valid'`` returns only the portion where the two arrays
    fully overlap:

    >>> jnp.convolve(x, y, mode='valid')
    Array([16., 15., 12.], dtype=float32)

    For complex-valued inputs:

    >>> x1 = jnp.array([3+1j, 2, 4-3j])
    >>> y1 = jnp.array([1, 2-3j, 4+5j])
    >>> jnp.convolve(x1, y1)
    Array([ 3. +1.j, 11. -7.j, 15.+10.j,  7. -8.j, 31. +8.j], dtype=complex64)
  """
  util.check_arraylike("convolve", a, v)
  return _conv(asarray(a), asarray(v), mode=mode, op='convolve',
               precision=precision, preferred_element_type=preferred_element_type)
