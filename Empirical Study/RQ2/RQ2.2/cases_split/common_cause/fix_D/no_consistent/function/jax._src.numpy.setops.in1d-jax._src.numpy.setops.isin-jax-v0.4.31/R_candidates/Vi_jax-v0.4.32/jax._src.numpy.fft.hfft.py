def hfft(a: ArrayLike, n: int | None = None,
         axis: int = -1, norm: str | None = None) -> Array:
  """Compute a 1-D FFT of an array whose spectrum has Hermitian symmetry.

  JAX implementation of :func:`numpy.fft.hfft`.

  Args:
    a: input array.
    n: optional, int. Specifies the dimension of the result along ``axis``. If
      not specified, ``n = 2*(m-1)``, where ``m`` is the dimension of ``a``
      along ``axis``.
    axis: optional, int, default=-1. Specifies the axis along which the transform
      is computed. If not specified, the transform is computed along axis -1.
    norm: optional, string. The normalization mode. "backward", "ortho" and "forward"
      are supported. Default is "backward".

  Returns:
    A real-valued array containing the one-dimensional discret Fourier transform
    of ``a`` by exploiting its inherent Hermitian-symmetry, having a dimension of
    ``n`` along ``axis``.

  See also:
    - :func:`jax.numpy.fft.ihfft`: Computes a one-dimensional inverse FFT of an
      array whose spectrum has Hermitian symmetry.
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.rfft`: Computes a one-dimensional discrete Fourier
      transform of a real-valued input.

  Examples:
    >>> x = jnp.array([[1, 3, 5, 7],
    ...                [2, 4, 6, 8]])
    >>> jnp.fft.hfft(x)
    Array([[24., -8.,  0., -2.,  0., -8.],
           [30., -8.,  0., -2.,  0., -8.]], dtype=float32)

    This value is equal to the real component of the discrete Fourier transform
    of the following array ``x1`` computed using ``jnp.fft.fft``.

    >>> x1 = jnp.array([[1, 3, 5, 7, 5, 3],
    ...                 [2, 4, 6, 8, 6, 4]])
    >>> jnp.fft.fft(x1)
    Array([[24.+0.j, -8.+0.j,  0.+0.j, -2.+0.j,  0.+0.j, -8.+0.j],
           [30.+0.j, -8.+0.j,  0.+0.j, -2.+0.j,  0.+0.j, -8.+0.j]],      dtype=complex64)
    >>> jnp.allclose(jnp.fft.hfft(x), jnp.fft.fft(x1))
    Array(True, dtype=bool)

    To obtain an odd-length output from ``jnp.fft.hfft``, ``n`` must be specified
    with an odd value, as the default behavior produces an even-length result
    along the specified ``axis``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.hfft(x, n=5))
    [[17.   -5.24 -0.76 -0.76 -5.24]
     [22.   -5.24 -0.76 -0.76 -5.24]]

    When ``n=3`` and ``axis=0``, dimension of the transform along ``axis 0`` will
    be ``3`` and dimension along other axes will be same as that of input.

    >>> jnp.fft.hfft(x, n=3, axis=0)
    Array([[ 5., 11., 17., 23.],
           [-1., -1., -1., -1.],
           [-1., -1., -1., -1.]], dtype=float32)

    ``x`` can be reconstructed (but of complex datatype) using ``jnp.fft.ihfft``
    from the result of ``jnp.fft.hfft``, only when ``n`` is specified as ``2*(m-1)``
    if `m` is even or ``2*m-1`` if ``m`` is odd, where ``m`` is the dimension of
    input along ``axis``.

    >>> jnp.fft.ihfft(jnp.fft.hfft(x, 2*(x.shape[-1]-1)))
    Array([[1.+0.j, 3.+0.j, 5.+0.j, 7.+0.j],
           [2.+0.j, 4.+0.j, 6.+0.j, 8.+0.j]], dtype=complex64)
    >>> jnp.allclose(x, jnp.fft.ihfft(jnp.fft.hfft(x, 2*(x.shape[-1]-1))))
    Array(True, dtype=bool)

    For complex-valued inputs:

    >>> x2 = jnp.array([[1+2j, 3-4j, 5+6j],
    ...                 [2-3j, 4+5j, 6-7j]])
    >>> jnp.fft.hfft(x2)
    Array([[ 12., -12.,   0.,   4.],
           [ 16.,   6.,   0., -14.]], dtype=float32)
  """
  conj_a = ufuncs.conj(a)
  _axis_check_1d('hfft', axis)
  nn = (conj_a.shape[axis] - 1) * 2 if n is None else n
  return _fft_core_1d('hfft', xla_client.FftType.IRFFT, conj_a, n=n, axis=axis,
                      norm=norm) * nn
