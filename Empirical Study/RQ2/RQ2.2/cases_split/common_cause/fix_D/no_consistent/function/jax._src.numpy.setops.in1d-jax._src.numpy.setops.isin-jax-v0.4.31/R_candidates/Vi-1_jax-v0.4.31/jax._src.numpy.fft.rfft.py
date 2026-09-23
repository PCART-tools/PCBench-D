def rfft(a: ArrayLike, n: int | None = None,
         axis: int = -1, norm: str | None = None) -> Array:
  r"""Compute a one-dimensional discrete Fourier transform of a real-valued array.

  JAX implementation of :func:`numpy.fft.rfft`.

  Args:
    a: real-valued input array.
    n: int. Specifies the effective dimension of the input along ``axis``. If not
      specified, it will default to the dimension of input along ``axis``.
    axis: int, default=-1. Specifies the axis along which the transform is computed.
      If not specified, the transform is computed along axis -1.
    norm: string. The normalization mode. "backward", "ortho" and "forward" are
      supported.

  Returns:
    An array containing the one-dimensional discrete Fourier transform of ``a``.
    The dimension of the array along ``axis`` is ``(n/2)+1``, if ``n`` is even and
    ``(n+1)/2``, if ``n`` is odd.

  See also:
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.irfft`: Computes a one-dimensional inverse discrete
      Fourier transform for real input.
    - :func:`jax.numpy.fft.rfftn`: Computes a multidimensional discrete Fourier
      transform for real input.
    - :func:`jax.numpy.fft.irfftn`: Computes a multidimensional inverse discrete
      Fourier transform for real input.

  Examples:
    ``jnp.fft.rfft`` computes the transform along ``axis -1`` by default.

    >>> x = jnp.array([[1, 3, 5],
    ...                [2, 4, 6]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfft(x)
    Array([[ 9.+0.j  , -3.+1.73j],
           [12.+0.j  , -3.+1.73j]], dtype=complex64)

    When ``n=5``, dimension of the transform along axis -1 will be ``(5+1)/2 =3``
    and dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfft(x, n=5)
    Array([[ 9.  +0.j  , -2.12-5.79j,  0.12+2.99j],
           [12.  +0.j  , -1.62-7.33j,  0.62+3.36j]], dtype=complex64)

    When ``n=4`` and ``axis=0``, dimension of the transform along ``axis 0`` will
    be ``(4/2)+1 =3`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfft(x, n=4, axis=0)
    Array([[ 3.+0.j,  7.+0.j, 11.+0.j],
           [ 1.-2.j,  3.-4.j,  5.-6.j],
           [-1.+0.j, -1.+0.j, -1.+0.j]], dtype=complex64)
  """
  return _fft_core_1d('rfft', xla_client.FftType.RFFT, a, n=n, axis=axis,
                      norm=norm)
