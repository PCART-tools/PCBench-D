def resize(image, shape: core.Shape, method: Union[str, ResizeMethod],
           antialias: bool = True,
           precision = lax.Precision.HIGHEST):
  """Image resize.

  The ``method`` argument expects one of the following resize methods:

  ``ResizeMethod.NEAREST``, ``"nearest"``
    `Nearest neighbor interpolation`_. The values of ``antialias`` and
    ``precision`` are ignored.

  ``ResizeMethod.LINEAR``, ``"linear"``, ``"bilinear"``, ``"trilinear"``, ``"triangle"``
    `Linear interpolation`_. If ``antialias`` is ``True``, uses a triangular
    filter when downsampling.

  ``ResizeMethod.CUBIC``, ``"cubic"``, ``"bicubic"``, ``"tricubic"``
    `Cubic interpolation`_, using the Keys cubic kernel.

  ``ResizeMethod.LANCZOS3``, ``"lanczos3"``
    `Lanczos resampling`_, using a kernel of radius 3.

  ``ResizeMethod.LANCZOS5``, ``"lanczos5"``
    `Lanczos resampling`_, using a kernel of radius 5.

  .. _Nearest neighbor interpolation: https://en.wikipedia.org/wiki/Nearest-neighbor_interpolation
  .. _Linear interpolation: https://en.wikipedia.org/wiki/Bilinear_interpolation
  .. _Cubic interpolation: https://en.wikipedia.org/wiki/Bicubic_interpolation
  .. _Lanczos resampling: https://en.wikipedia.org/wiki/Lanczos_resampling

  Args:
    image: a JAX array.
    shape: the output shape, as a sequence of integers with length equal to
      the number of dimensions of `image`. Note that :func:`resize` does not
      distinguish spatial dimensions from batch or channel dimensions, so this
      includes all dimensions of the image. To represent a batch or a channel
      dimension, simply leave that element of the shape unchanged.
    method: the resizing method to use; either a ``ResizeMethod`` instance or a
      string. Available methods are: LINEAR, LANCZOS3, LANCZOS5, CUBIC.
    antialias: should an antialiasing filter be used when downsampling? Defaults
      to ``True``. Has no effect when upsampling.
  Returns:
    The resized image.
  """
  return _resize(image, core.canonicalize_shape(shape), method, antialias,
                 precision)
