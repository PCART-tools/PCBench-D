def irfft2(a: ArrayLike, s: Shape | None = None, axes: Sequence[int] = (-2,-1),
           norm: str | None = None) -> Array:
  """Compute a real-valued two-dimensional inverse discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.irfft2`.

  Args:
    a: input array. Must have ``a.ndim >= 2``.
    s: optional length-2 sequence of integers. Specifies the size of the output
      in each specified axis. If not specified, the dimension of output along
      axis ``axes[1]`` is ``2*(m-1)``, ``m`` is the size of input along axis
      ``axes[1]`` and the dimension along other axes will be the same as that of
      input.
    axes: optional length-2 sequence of integers, default=(-2,-1). Specifies the
      axes along which the transform is computed.
    norm: string, default="backward". The normalization mode. "backward", "ortho"
      and "forward" are supported.

  Returns:
    A real-valued array containing the two-dimensional inverse discrete Fourier
    transform of ``a``.

  See also:
    - :func:`jax.numpy.fft.rfft2`: Computes a two-dimensional discrete Fourier
      transform of a real-valued array.
    - :func:`jax.numpy.fft.irfft`: Computes a real-valued one-dimensional inverse
      discrete Fourier transform.
    - :func:`jax.numpy.fft.irfftn`: Computes a real-valued multidimensional inverse
      discrete Fourier transform.

  Examples:
    ``jnp.fft.irfft2`` computes the transform along the last two axes by default.

    >>> x = jnp.array([[[1, 3, 5],
    ...                 [2, 4, 6]],
    ...                [[7, 9, 11],
    ...                 [8, 10, 12]]])
    >>> jnp.fft.irfft2(x)
    Array([[[ 3.5, -1. ,  0. , -1. ],
            [-0.5,  0. ,  0. ,  0. ]],
    <BLANKLINE>
           [[ 9.5, -1. ,  0. , -1. ],
            [-0.5,  0. ,  0. ,  0. ]]], dtype=float32)

    When ``s=[3, 3]``, dimension of the transform along ``axes (-2, -1)`` will be
    ``(3, 3)`` and dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.irfft2(x, s=[3, 3])
    Array([[[ 1.89, -0.44, -0.44],
            [ 0.22, -0.78,  0.56],
            [ 0.22,  0.56, -0.78]],
    <BLANKLINE>
           [[ 5.89, -0.44, -0.44],
            [ 1.22, -1.78,  1.56],
            [ 1.22,  1.56, -1.78]]], dtype=float32)

    When ``s=[2, 3]`` and ``axes=(0, 1)``, shape of the transform along
    ``axes (0, 1)`` will be ``(2, 3)`` and dimension along other axes will be
    same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.irfft2(x, s=[2, 3], axes=(0, 1))
    Array([[[ 4.67,  6.67,  8.67],
            [-0.33, -0.33, -0.33],
            [-0.33, -0.33, -0.33]],
    <BLANKLINE>
           [[-3.  , -3.  , -3.  ],
            [ 0.  ,  0.  ,  0.  ],
            [ 0.  ,  0.  ,  0.  ]]], dtype=float32)
  """
  return _fft_core_2d('irfft2', xla_client.FftType.IRFFT, a, s=s, axes=axes,
                      norm=norm)
