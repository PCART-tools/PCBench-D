def ifft(a: ArrayLike, n: int | None = None,
         axis: int = -1, norm: str | None = None) -> Array:
  r"""Compute a one-dimensional inverse discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.ifft`.

  Args:
    a: input array
    n: int. Specifies the dimension of the result along ``axis``. If not specified,
      it will default to the dimension of ``a`` along ``axis``.
    axis: int, default=-1. Specifies the axis along which the transform is computed.
      If not specified, the transform is computed along axis -1.
    norm: string. The normalization mode. "backward", "ortho" and "forward" are
      supported.

  Returns:
    An array containing the one-dimensional discrete Fourier transform of ``a``.

  See also:
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.fftn`: Computes a multidimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.ifftn`: Computes a multidimensional inverse of discrete
      Fourier transform.

  Examples:
    ``jnp.fft.ifft`` computes the transform along ``axis -1`` by default.

    >>> x = jnp.array([[3, 1, 4, 6],
    ...                [2, 5, 7, 1]])
    >>> jnp.fft.ifft(x)
    Array([[ 3.5 +0.j  , -0.25-1.25j,  0.  +0.j  , -0.25+1.25j],
          [ 3.75+0.j  , -1.25+1.j  ,  0.75+0.j  , -1.25-1.j  ]],      dtype=complex64)

    When ``n=5``, dimension of the transform along axis -1 will be ``5`` and
    dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.ifft(x, n=5))
    [[ 2.8 +0.j   -0.96-0.04j  1.06+0.5j   1.06-0.5j  -0.96+0.04j]
     [ 3.  +0.j   -0.59+1.66j  0.09-0.55j  0.09+0.55j -0.59-1.66j]]

    When ``n=3`` and ``axis=0``, dimension of the transform along ``axis 0`` will
    be ``3`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.ifft(x, n=3, axis=0))
    [[ 1.67+0.j    2.  +0.j    3.67+0.j    2.33+0.j  ]
     [ 0.67+0.58j -0.5 +1.44j  0.17+2.02j  1.83+0.29j]
     [ 0.67-0.58j -0.5 -1.44j  0.17-2.02j  1.83-0.29j]]
  """
  return _fft_core_1d('ifft', xla_client.FftType.IFFT, a, n=n, axis=axis,
                      norm=norm)
