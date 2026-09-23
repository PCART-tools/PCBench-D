def ihfft(a: ArrayLike, n: int | None = None,
          axis: int = -1, norm: str | None = None) -> Array:
  r"""Compute a 1-D inverse FFT of an array whose spectrum has Hermitian-symmetry.

  JAX implementation of :func:`numpy.fft.ihfft`.

  Args:
    a: input array.
    n: optional, int. Specifies the effective dimension of the input along ``axis``.
      If not specified, it will default to the dimension of input along ``axis``.
    axis: optional, int, default=-1. Specifies the axis along which the transform
      is computed. If not specified, the transform is computed along axis -1.
    norm: optional, string. The normalization mode. "backward", "ortho" and "forward"
      are supported. Default is "backward".

  Returns:
    An array containing one-dimensional discrete Fourier transform of ``a`` by
    exploiting its inherent Hermitian symmetry. The dimension of the array along
    ``axis`` is ``(n/2)+1``, if ``n`` is even and ``(n+1)/2``, if ``n`` is odd.

  See also:
    - :func:`jax.numpy.fft.hfft`: Computes a one-dimensional FFT of an array
      whose spectrum has Hermitian symmetry.
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.rfft`: Computes a one-dimensional discrete Fourier
      transform of a real-valued input.

  Examples:
    >>> x = jnp.array([[1, 3, 5, 7],
    ...                [2, 4, 6, 8]])
    >>> jnp.fft.ihfft(x)
    Array([[ 4.+0.j, -1.-1.j, -1.-0.j],
           [ 5.+0.j, -1.-1.j, -1.-0.j]], dtype=complex64)

    When ``n=4`` and ``axis=0``, dimension of the transform along ``axis 0`` will
    be ``(4/2)+1 =3`` and dimension along other axes will be same as that of input.

    >>> jnp.fft.ihfft(x, n=4, axis=0)
    Array([[ 0.75+0.j ,  1.75+0.j ,  2.75+0.j ,  3.75+0.j ],
           [ 0.25+0.5j,  0.75+1.j ,  1.25+1.5j,  1.75+2.j ],
           [-0.25-0.j , -0.25-0.j , -0.25-0.j , -0.25-0.j ]], dtype=complex64)
  """
  _axis_check_1d('ihfft', axis)
  arr = jnp.asarray(a)
  nn = arr.shape[axis] if n is None else n
  output = _fft_core_1d('ihfft', xla_client.FftType.RFFT, arr, n=n, axis=axis,
                        norm=norm)
  return ufuncs.conj(output) * (1 / nn)
