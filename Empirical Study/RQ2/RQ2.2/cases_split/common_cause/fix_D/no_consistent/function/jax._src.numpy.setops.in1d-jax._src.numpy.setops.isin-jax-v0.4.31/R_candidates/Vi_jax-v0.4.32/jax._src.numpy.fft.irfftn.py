def irfftn(a: ArrayLike, s: Shape | None = None,
           axes: Sequence[int] | None = None,
           norm: str | None = None) -> Array:
  """Compute a real-valued multidimensional inverse discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.irfftn`.

  Args:
    a: input array.
    s: optional sequence of integers. Specifies the size of the output in each
      specified axis. If not specified, the dimension of output along axis
      ``axes[-1]`` is ``2*(m-1)``, ``m`` is the size of input along axis ``axes[-1]``
      and the dimension along other axes will be the same as that of input.
    axes: optional sequence of integers, default=None. Specifies the axes along
      which the transform is computed. If not specified, the transform is computed
      along the last ``len(s)`` axes. If neither ``axes`` nor ``s`` is specified,
      the transform is computed along all the axes.
    norm: string, default="backward". The normalization mode. "backward", "ortho"
      and "forward" are supported.

  Returns:
    A real-valued array containing the multidimensional inverse discrete Fourier
    transform of ``a`` with size ``s`` along specified ``axes``, and the same as
    the input along other axes.

  See also:
    - :func:`jax.numpy.fft.rfftn`: Computes a multidimensional discrete Fourier
      transform of a real-valued array.
    - :func:`jax.numpy.fft.irfft`: Computes a real-valued one-dimensional inverse
      discrete Fourier transform.
    - :func:`jax.numpy.fft.irfft2`: Computes a real-valued two-dimensional inverse
      discrete Fourier transform.

  Examples:
    ``jnp.fft.irfftn`` computes the transform along all the axes by default.

    >>> x = jnp.array([[[1, 3, 5],
    ...                 [2, 4, 6]],
    ...                [[7, 9, 11],
    ...                 [8, 10, 12]]])
    >>> jnp.fft.irfftn(x)
    Array([[[ 6.5, -1. ,  0. , -1. ],
            [-0.5,  0. ,  0. ,  0. ]],
    <BLANKLINE>
           [[-3. ,  0. ,  0. ,  0. ],
            [ 0. ,  0. ,  0. ,  0. ]]], dtype=float32)

    When ``s=[3, 4]``, size of the transform along ``axes (-2, -1)`` will be
    ``(3, 4)`` and size along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.irfftn(x, s=[3, 4])
    Array([[[ 2.33, -0.67,  0.  , -0.67],
            [ 0.33, -0.74,  0.  ,  0.41],
            [ 0.33,  0.41,  0.  , -0.74]],
    <BLANKLINE>
           [[ 6.33, -0.67,  0.  , -0.67],
            [ 1.33, -1.61,  0.  ,  1.28],
            [ 1.33,  1.28,  0.  , -1.61]]], dtype=float32)

    When ``s=[3]`` and ``axes=[0]``, size of the transform along ``axes 0`` will
    be ``3`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.irfftn(x, s=[3], axes=[0])
    Array([[[ 5.,  7.,  9.],
            [ 6.,  8., 10.]],
    <BLANKLINE>
           [[-2., -2., -2.],
            [-2., -2., -2.]],
    <BLANKLINE>
           [[-2., -2., -2.],
            [-2., -2., -2.]]], dtype=float32)
  """
  return _fft_core('irfftn', xla_client.FftType.IRFFT, a, s, axes, norm)
