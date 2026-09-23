def rfft2(a: ArrayLike, s: Shape | None = None, axes: Sequence[int] = (-2,-1),
          norm: str | None = None) -> Array:
  """Compute a two-dimensional discrete Fourier transform of a real-valued array.

  JAX implementation of :func:`numpy.fft.rfft2`.

  Args:
    a: real-valued input array. Must have ``a.ndim >= 2``.
    s: optional length-2 sequence of integers. Specifies the effective size of the
      output along each specified axis. If not specified, it will default to the
      dimension of input along ``axes``.
    axes: optional length-2 sequence of integers, default=(-2,-1). Specifies the
      axes along which the transform is computed.
    norm: string, default="backward". The normalization mode. "backward", "ortho"
      and "forward" are supported.

  Returns:
    An array containing the two-dimensional discrete Fourier transform of ``a``.
    The size of the output along the axis ``axes[1]`` is ``(s[1]/2)+1``, if ``s[1]``
    is even and ``(s[1]+1)/2``, if ``s[1]`` is odd. The size of the output along
    the axis ``axes[0]`` is ``s[0]``.

  See also:
    - :func:`jax.numpy.fft.rfft`: Computes a one-dimensional discrete Fourier
      transform of real-valued array.
    - :func:`jax.numpy.fft.rfftn`: Computes a multidimensional discrete Fourier
      transform of real-valued array.
    - :func:`jax.numpy.fft.irfft2`: Computes a real-valued two-dimensional inverse
      discrete Fourier transform.

  Examples:
    ``jnp.fft.rfft2`` computes the transform along the last two axes by default.

    >>> x = jnp.array([[[1, 3, 5],
    ...                 [2, 4, 6]],
    ...                [[7, 9, 11],
    ...                 [8, 10, 12]]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfft2(x)
    Array([[[21.+0.j  , -6.+3.46j],
            [-3.+0.j  ,  0.+0.j  ]],
    <BLANKLINE>
           [[57.+0.j  , -6.+3.46j],
            [-3.+0.j  ,  0.+0.j  ]]], dtype=complex64)

    When ``s=[2, 4]``, dimension of the transform along ``axis -2`` will be
    ``2``, along ``axis -1`` will be ``(4/2)+1) = 3`` and dimension along other
    axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfft2(x, s=[2, 4])
    Array([[[21. +0.j, -8. -7.j,  7. +0.j],
            [-3. +0.j,  0. +1.j, -1. +0.j]],
    <BLANKLINE>
           [[57. +0.j, -8.-19.j, 19. +0.j],
            [-3. +0.j,  0. +1.j, -1. +0.j]]], dtype=complex64)

    When ``s=[3, 5]`` and ``axes=(0, 1)``, shape of the transform along ``axis 0``
    will be ``3``, along ``axis 1`` will be ``(5+1)/2 = 3`` and dimension along
    other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfft2(x, s=[3, 5], axes=(0, 1))
    Array([[[ 18.   +0.j  ,  26.   +0.j  ,  34.   +0.j  ],
            [ 11.09 -9.51j,  16.33-13.31j,  21.56-17.12j],
            [ -0.09 -5.88j,   0.67 -8.23j,   1.44-10.58j]],
    <BLANKLINE>
          [[ -4.5 -12.99j,  -2.5 -16.45j,  -0.5 -19.92j],
            [ -9.71 -6.3j , -10.05 -9.52j, -10.38-12.74j],
            [ -4.95 +0.72j,  -5.78 -0.2j ,  -6.61 -1.12j]],
    <BLANKLINE>
          [[ -4.5 +12.99j,  -2.5 +16.45j,  -0.5 +19.92j],
            [  3.47+10.11j,   6.43+11.42j,   9.38+12.74j],
            [  3.19 +1.63j,   4.4  +1.38j,   5.61 +1.12j]]], dtype=complex64)
  """
  return _fft_core_2d('rfft2', xla_client.FftType.RFFT, a, s=s, axes=axes,
                      norm=norm)
