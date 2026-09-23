class ResizeMethod(enum.Enum):
  """Image resize method.

  Possible values are:

  NEAREST:
    Nearest-neighbor interpolation.

  LINEAR:
    `Linear interpolation`_.

  LANCZOS3:
    `Lanczos resampling`_, using a kernel of radius 3.

  LANCZOS5:
    `Lanczos resampling`_, using a kernel of radius 5.

  CUBIC:
    `Cubic interpolation`_, using the Keys cubic kernel.

  .. _Linear interpolation: https://en.wikipedia.org/wiki/Bilinear_interpolation
  .. _Cubic interpolation: https://en.wikipedia.org/wiki/Bicubic_interpolation
  .. _Lanczos resampling: https://en.wikipedia.org/wiki/Lanczos_resampling
  """

  NEAREST = 0
  LINEAR = 1
  LANCZOS3 = 2
  LANCZOS5 = 3
  CUBIC = 4

  # Caution: The current resize implementation assumes that the resize kernels
  # are interpolating, i.e. for the identity warp the output equals the input.
  # This is not true for, e.g. a Gaussian kernel, so if such kernels are added
  # the implementation will need to be changed.

  @staticmethod
  def from_string(s: str):
    if s == 'nearest':
      return ResizeMethod.NEAREST
    if s in ['linear', 'bilinear', 'trilinear', 'triangle']:
      return ResizeMethod.LINEAR
    elif s == 'lanczos3':
      return ResizeMethod.LANCZOS3
    elif s == 'lanczos5':
      return ResizeMethod.LANCZOS5
    elif s in ['cubic', 'bicubic', 'tricubic']:
      return ResizeMethod.CUBIC
    else:
      raise ValueError(f'Unknown resize method "{s}"')
