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
