def is_constant_dim(d: DimSize) -> bool:
  # Whether the dimension is a static integer constant.
  try:
    operator.index(d)
    return True
  except:
    return False
