  @staticmethod
  def convert_from(bint_dtype, other_dtype) -> bool:
    return other_dtype in (np.dtype('int32'), np.dtype('int64'))
