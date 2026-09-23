def ifft2(a: ArrayLike, s: Shape | None = None, axes: Sequence[int] = (-2,-1),
          norm: str | None = None) -> Array:
  """Compute a two-dimensional inverse discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.ifft2`.

  Args:
    a: input array. Must have ``a.ndim >= 2``.
    s: optional length-2 sequence of integers. Specifies the size of the output
      in each specified axis. If not specified, it will default to the size of
      ``a`` along the specified ``axes``.
    axes: optional length-2 sequence of integers, default=(-2,-1). Specifies the
      axes along which the transform is computed.
    norm: string, default="backward". The normalization mode. "backward", "ortho"
      and "forward" are supported.

  Returns:
    An array containing the two-dimensional inverse discrete Fourier transform
    of ``a`` along given ``axes``.

  See also:
    - :func:`jax.numpy.fft.ifft`: Computes a one-dimensional inverse discrete
      Fourier transform.
    - :func:`jax.numpy.fft.ifftn`: Computes a multidimensional inverse discrete
      Fourier transform.
    - :func:`jax.numpy.fft.fft2`: Computes a two-dimensional discrete Fourier
      transform.

  Examples:
    ``jnp.fft.ifft2`` computes the transform along the last two axes by default.

    >>> x = jnp.array([[[1, 3],
    ...                 [2, 4]],
    ...                [[5, 7],
    ...                 [6, 8]]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.ifft2(x)
    Array([[[ 2.5+0.j, -1. +0.j],
            [-0.5+0.j,  0. +0.j]],
    <BLANKLINE>
           [[ 6.5+0.j, -1. +0.j],
            [-0.5+0.j,  0. +0.j]]], dtype=complex64)

    When ``s=[2, 3]``, dimension of the transform along ``axes (-2, -1)`` will be
    ``(2, 3)`` and dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.ifft2(x, s=[2, 3])
    Array([[[ 1.67+0.j  , -0.08+1.01j, -0.08-1.01j],
            [-0.33+0.j  , -0.08-0.14j, -0.08+0.14j]],
    <BLANKLINE>
           [[ 4.33+0.j  ,  0.58+2.17j,  0.58-2.17j],
            [-0.33+0.j  , -0.08-0.14j, -0.08+0.14j]]], dtype=complex64)

    When ``s=[2, 3]`` and ``axes=(0, 1)``, shape of the transform along
    ``axes (0, 1)`` will be ``(2, 3)`` and dimension along other axes will be
    same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.ifft2(x, s=[2, 3], axes=(0, 1))
    Array([[[ 2.33+0.j  ,  3.67+0.j  ],
            [ 0.33+1.15j,  0.67+1.73j],
            [ 0.33-1.15j,  0.67-1.73j]],
    <BLANKLINE>
           [[-1.33+0.j  , -1.33+0.j  ],
            [-0.33-0.58j, -0.33-0.58j],
            [-0.33+0.58j, -0.33+0.58j]]], dtype=complex64)
  """
  return _fft_core_2d('ifft2', xla_client.FftType.IFFT, a, s=s, axes=axes,
                      norm=norm)
