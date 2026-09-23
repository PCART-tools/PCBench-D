def check_bool_conversion(arr: Array, warn_on_empty=False):
  if arr.size == 0:
    if warn_on_empty:
      warnings.warn(
        "The truth value of an empty array is ambiguous. Returning False. In the future this "
        "will result in an error. Use `array.size > 0` to check that an array is not empty.",
        DeprecationWarning, stacklevel=3)
    else:
      raise ValueError("The truth value of an empty array is ambiguous. Use "
                       "`array.size > 0` to check that an array is not empty.")
  if arr.size > 1:
    raise ValueError("The truth value of an array with more than one element is "
                      "ambiguous. Use a.any() or a.all()")
