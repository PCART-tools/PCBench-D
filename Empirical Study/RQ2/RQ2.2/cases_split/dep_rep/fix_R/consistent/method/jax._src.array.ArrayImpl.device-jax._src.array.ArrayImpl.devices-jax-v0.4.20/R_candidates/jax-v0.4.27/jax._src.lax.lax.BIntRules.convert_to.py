  @staticmethod
  def convert_to(other_dtype, bint_dtype) -> bool:
    return other_dtype in (np.dtype('int32'), np.dtype('int64'))
