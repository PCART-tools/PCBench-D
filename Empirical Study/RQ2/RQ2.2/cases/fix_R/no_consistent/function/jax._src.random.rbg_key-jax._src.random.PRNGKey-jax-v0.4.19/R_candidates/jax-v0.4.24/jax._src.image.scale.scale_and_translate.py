def scale_and_translate(image, shape: core.Shape,
                        spatial_dims: Sequence[int],
                        scale, translation,
                        method: str | ResizeMethod,
                        antialias: bool = True,
                        precision=lax.Precision.HIGHEST):
  """Apply a scale and translation to an image.

  Generates a new image of shape 'shape' by resampling from the input image
  using the sampling method corresponding to method. For 2D images, this
  operation transforms a location in the input images, (x, y), to a location
  in the output image according to::

    (x * scale[1] + translation[1], y * scale[0] + translation[0])

  (Note the *inverse* warp is used to generate the sample locations.)
  Assumes half-centered pixels, i.e the pixel at integer location ``row, col``
  has coordinates ``y, x = row + 0.5, col + 0.5``, and similarly for other input
  image dimensions.

  If an output location(pixel) maps to an input sample location that is outside
  the input boundaries then the value for the output location will be set to
  zero.

  The ``method`` argument expects one of the following resize methods:

  ``ResizeMethod.LINEAR``, ``"linear"``, ``"bilinear"``, ``"trilinear"``,
    ``"triangle"`` `Linear interpolation`_. If ``antialias`` is ``True``, uses a
    triangular filter when downsampling.

  ``ResizeMethod.CUBIC``, ``"cubic"``, ``"bicubic"``, ``"tricubic"``
    `Cubic interpolation`_, using the Keys cubic kernel.

  ``ResizeMethod.LANCZOS3``, ``"lanczos3"``
    `Lanczos resampling`_, using a kernel of radius 3.

  ``ResizeMethod.LANCZOS5``, ``"lanczos5"``
    `Lanczos resampling`_, using a kernel of radius 5.

  .. _Linear interpolation: https://en.wikipedia.org/wiki/Bilinear_interpolation
  .. _Cubic interpolation: https://en.wikipedia.org/wiki/Bicubic_interpolation
  .. _Lanczos resampling: https://en.wikipedia.org/wiki/Lanczos_resampling

  Args:
    image: a JAX array.
    shape: the output shape, as a sequence of integers with length equal to the
      number of dimensions of `image`.
    spatial_dims: A length K tuple specifying the spatial dimensions that the
      passed scale and translation should be applied to.
    scale: A [K] array with the same number of dimensions as image, containing
      the scale to apply in each dimension.
    translation: A [K] array with the same number of dimensions as image,
      containing the translation to apply in each dimension.
    method: the resizing method to use; either a ``ResizeMethod`` instance or a
      string. Available methods are: LINEAR, LANCZOS3, LANCZOS5, CUBIC.
    antialias: Should an antialiasing filter be used when downsampling? Defaults
      to ``True``. Has no effect when upsampling.

  Returns:
    The scale and translated image.
  """
  shape = core.canonicalize_shape(shape)
  if len(shape) != image.ndim:
    msg = ('shape must have length equal to the number of dimensions of x; '
           f' {shape} vs {image.shape}')
    raise ValueError(msg)
  if isinstance(method, str):
    method = ResizeMethod.from_string(method)
  if method == ResizeMethod.NEAREST:
    # Nearest neighbor is currently special-cased for straight resize, so skip
    # for now.
    raise ValueError('Nearest neighbor resampling is not currently supported '
                     'for scale_and_translate.')
  assert isinstance(method, ResizeMethod)

  kernel = _kernels[method]
  image, = promote_dtypes_inexact(image)
  scale, translation = promote_dtypes_inexact(scale, translation)
  return _scale_and_translate(image, shape, spatial_dims, scale, translation,
                              kernel, antialias, precision)
