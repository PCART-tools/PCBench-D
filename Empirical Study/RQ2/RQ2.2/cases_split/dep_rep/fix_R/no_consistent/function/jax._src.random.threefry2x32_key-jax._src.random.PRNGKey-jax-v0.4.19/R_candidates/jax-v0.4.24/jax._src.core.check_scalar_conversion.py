def check_scalar_conversion(arr: Array):
  if arr.size != 1:
    raise TypeError("Only length-1 arrays can be converted to Python scalars.")
  if arr.shape != ():
    # Added 2023 September 18.
    warnings.warn("Conversion of an array with ndim > 0 to a scalar is deprecated, "
                  "and will error in future.", DeprecationWarning, stacklevel=3)
