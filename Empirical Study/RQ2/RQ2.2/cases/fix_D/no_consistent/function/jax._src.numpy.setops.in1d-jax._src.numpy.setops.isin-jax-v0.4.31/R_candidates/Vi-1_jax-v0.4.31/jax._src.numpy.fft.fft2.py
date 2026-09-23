def fft2(a: ArrayLike, s: Shape | None = None, axes: Sequence[int] = (-2,-1),
         norm: str | None = None) -> Array:
  """Compute a two-dimensional discrete Fourier transform along given axes.

  JAX implementation of :func:`numpy.fft.fft2`.

  Args:
    a: input array. Must have ``a.ndim >= 2``.
    s: optional length-2 sequence of integers. Specifies the size of the output
      along each specified axis. If not specified, it will default to the size
      of ``a`` along the specified ``axes``.
    axes: optional length-2 sequence of integers, default=(-2,-1). Specifies the
      axes along which the transform is computed.
    norm: string, default="backward". The normalization mode. "backward", "ortho"
      and "forward" are supported.

  Returns:
    An array containing the two-dimensional discrete Fourier transform of ``a``
    along given ``axes``.

  See also:
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.fftn`: Computes a multidimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.ifft2`: Computes a two-dimensional inverse discrete
      Fourier transform.

  Examples:
    ``jnp.fft.fft2`` computes the transform along the last two axes by default.

    >>> x = jnp.array([[[1, 3],
    ...                 [2, 4]],
    ...                [[5, 7],
    ...                 [6, 8]]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.fft2(x)
    Array([[[10.+0.j, -4.+0.j],
            [-2.+0.j,  0.+0.j]],
    <BLANKLINE>
           [[26.+0.j, -4.+0.j],
            [-2.+0.j,  0.+0.j]]], dtype=complex64)

    When ``s=[2, 3]``, dimension of the transform along ``axes (-2, -1)`` will be
    ``(2, 3)`` and dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.fft2(x, s=[2, 3])
    Array([[[10.  +0.j  , -0.5 -6.06j, -0.5 +6.06j],
            [-2.  +0.j  , -0.5 +0.87j, -0.5 -0.87j]],
    <BLANKLINE>
           [[26.  +0.j  ,  3.5-12.99j,  3.5+12.99j],
            [-2.  +0.j  , -0.5 +0.87j, -0.5 -0.87j]]], dtype=complex64)

    When ``s=[2, 3]`` and ``axes=(0, 1)``, shape of the transform along
    ``axes (0, 1)`` will be ``(2, 3)`` and dimension along other axes will be
    same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.fft2(x, s=[2, 3], axes=(0, 1))
    Array([[[14. +0.j  , 22. +0.j  ],
            [ 2. -6.93j,  4.-10.39j],
            [ 2. +6.93j,  4.+10.39j]],
    <BLANKLINE>
           [[-8. +0.j  , -8. +0.j  ],
            [-2. +3.46j, -2. +3.46j],
            [-2. -3.46j, -2. -3.46j]]], dtype=complex64)

    ``jnp.fft.ifft2`` can be used to reconstruct ``x`` from the result of
    ``jnp.fft.fft2``.

    >>> x_fft2 = jnp.fft.fft2(x)
    >>> jnp.allclose(x, jnp.fft.ifft2(x_fft2))
    Array(True, dtype=bool)
  """
  return _fft_core_2d('fft2', xla_client.FftType.FFT, a, s=s, axes=axes,
                      norm=norm)
