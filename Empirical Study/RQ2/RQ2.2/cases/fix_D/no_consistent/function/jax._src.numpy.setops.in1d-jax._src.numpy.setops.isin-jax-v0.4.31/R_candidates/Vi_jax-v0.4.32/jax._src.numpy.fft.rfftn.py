def rfftn(a: ArrayLike, s: Shape | None = None,
          axes: Sequence[int] | None = None,
          norm: str | None = None) -> Array:
  """Compute a multidimensional discrete Fourier transform of a real-valued array.

  JAX implementation of :func:`numpy.fft.rfftn`.

  Args:
    a: real-valued input array.
    s: optional sequence of integers. Controls the effective size of the input
      along each specified axis. If not specified, it will default to the
      dimension of input along ``axes``.
    axes: optional sequence of integers, default=None. Specifies the axes along
      which the transform is computed. If not specified, the transform is computed
      along the last ``len(s)`` axes. If neither ``axes`` nor ``s`` is specified,
      the transform is computed along all the axes.
    norm: string, default="backward". The normalization mode. "backward", "ortho"
      and "forward" are supported.

  Returns:
    An array containing the multidimensional discrete Fourier transform of ``a``
    having size specified in ``s`` along the axes ``axes`` except along the axis
    ``axes[-1]``. The size of the output along the axis ``axes[-1]`` is
    ``s[-1]//2+1``.

  See also:
    - :func:`jax.numpy.fft.rfft`: Computes a one-dimensional discrete Fourier
      transform of real-valued array.
    - :func:`jax.numpy.fft.rfft2`: Computes a two-dimensional discrete Fourier
      transform of real-valued array.
    - :func:`jax.numpy.fft.irfftn`: Computes a real-valued multidimensional inverse
      discrete Fourier transform.

  Examples:
    >>> x = jnp.array([[[1, 3, 5],
    ...                 [2, 4, 6]],
    ...                [[7, 9, 11],
    ...                 [8, 10, 12]]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfftn(x)
    Array([[[ 78.+0.j  , -12.+6.93j],
            [ -6.+0.j  ,   0.+0.j  ]],
    <BLANKLINE>
           [[-36.+0.j  ,   0.+0.j  ],
            [  0.+0.j  ,   0.+0.j  ]]], dtype=complex64)

    When ``s=[3, 3, 4]``,  size of the transform along ``axes (-3, -2)`` will
    be (3, 3), and along ``axis -1`` will be ``4//2+1 = 3`` and size along
    other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfftn(x, s=[3, 3, 4])
    Array([[[ 78.   +0.j  , -16.  -26.j  ,  26.   +0.j  ],
            [ 15.  -36.37j, -16.12 +1.93j,   5.  -12.12j],
            [ 15.  +36.37j,   8.12-11.93j,   5.  +12.12j]],
    <BLANKLINE>
           [[ -7.5 -49.36j, -20.45 +9.43j,  -2.5 -16.45j],
            [-25.5  -7.79j,  -0.6 +11.96j,  -8.5  -2.6j ],
            [ 19.5 -12.99j,  -8.33 -6.5j ,   6.5  -4.33j]],
    <BLANKLINE>
           [[ -7.5 +49.36j,  12.45 -4.43j,  -2.5 +16.45j],
            [ 19.5 +12.99j,   0.33 -6.5j ,   6.5  +4.33j],
            [-25.5  +7.79j,   4.6  +5.04j,  -8.5  +2.6j ]]], dtype=complex64)

    When ``s=[3, 5]`` and ``axes=(0, 1)``, size of the transform along ``axis 0``
    will be ``3``, along ``axis 1`` will be ``5//2+1 = 3`` and dimension along
    other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.rfftn(x, s=[3, 5], axes=[0, 1])
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

    For 1-D input:

    >>> x1 = jnp.array([1, 2, 3, 4])
    >>> jnp.fft.rfftn(x1)
    Array([10.+0.j, -2.+2.j, -2.+0.j], dtype=complex64)
  """
  return _fft_core('rfftn', xla_client.FftType.RFFT, a, s, axes, norm)
