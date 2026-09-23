def ifftn(a: ArrayLike, s: Shape | None = None,
          axes: Sequence[int] | None = None,
          norm: str | None = None) -> Array:
  r"""Compute a multidimensional inverse discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.ifftn`.

  Args:
    a: input array
    s: sequence of integers. Specifies the shape of the result. If not specified,
      it will default to the shape of ``a`` along the specified ``axes``.
    axes: sequence of integers, default=None. Specifies the axes along which the
      transform is computed. If None, computes the transform along all the axes.
    norm: string. The normalization mode. "backward", "ortho" and "forward" are
      supported.

  Returns:
    An array containing the multidimensional inverse discrete Fourier transform
    of ``a``.

  See also:
    - :func:`jax.numpy.fft.fftn`: Computes a multidimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.fft`: Computes a one-dimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.ifft`: Computes a one-dimensional inverse discrete
      Fourier transform.

  Examples:
    ``jnp.fft.ifftn`` computes the transform along all the axes by default when
    ``axes`` argument is ``None``.

    >>> x = jnp.array([[1, 2, 5, 3],
    ...                [4, 1, 2, 6],
    ...                [5, 3, 2, 1]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.ifftn(x))
    [[ 2.92+0.j    0.08-0.33j  0.25+0.j    0.08+0.33j]
     [-0.08+0.14j -0.04-0.03j  0.  -0.29j -1.05-0.11j]
     [-0.08-0.14j -1.05+0.11j  0.  +0.29j -0.04+0.03j]]

    When ``s=[3]``, dimension of the transform along ``axis -1`` will be ``3``
    and dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.ifftn(x, s=[3]))
    [[ 2.67+0.j   -0.83-0.87j -0.83+0.87j]
     [ 2.33+0.j    0.83-0.29j  0.83+0.29j]
     [ 3.33+0.j    0.83+0.29j  0.83-0.29j]]

    When ``s=[2]`` and ``axes=[0]``, dimension of the transform along ``axis 0``
    will be ``2`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.ifftn(x, s=[2], axes=[0]))
    [[ 2.5+0.j  1.5+0.j  3.5+0.j  4.5+0.j]
     [-1.5+0.j  0.5+0.j  1.5+0.j -1.5+0.j]]

    When ``s=[2, 3]``, shape of the transform will be ``(2, 3)``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.ifftn(x, s=[2, 3]))
    [[ 2.5 +0.j    0.  -0.58j  0.  +0.58j]
     [ 0.17+0.j   -0.83-0.29j -0.83+0.29j]]
  """
  return _fft_core('ifftn', xla_client.FftType.IFFT, a, s, axes, norm)
