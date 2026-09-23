def _float_to_int_for_sort(x):
  # Switch from a floating point value to a integer value in such a way that
  # when using the integer value to compare, we get the same result for normal
  # values, and -nan is treated as the smallest value, and nan is treated as
  # the largest value.
  # If f is a float, and
  # x = bit_cast<int32>(f);
  # y = x < 0 ? int32_max - x : x;
  # then y is ordered as an int32 such that finite values have the obvious
  # order. In this scheme, -0 would be before 0, and -NaN and NaN appear at
  # the beginning and end of the ordering. This causes issues for stable
  # sorts, so we avoid this by standardizing the representation of zeros
  # and NaNs in the output.
  # Note that in order to avoid -x to overflow, we calculate
  # int32_max - x as unsigned, and then convert back to signed.
  if x.dtype == dtypes.bfloat16:
    x = convert_element_type(x, np.float32)
  nbits = np.finfo(x).bits
  signed_dtype = _INT_DTYPES[nbits]
  unsigned_dtype = _UINT_DTYPES[nbits]

  signed = bitcast_convert_type(x, signed_dtype)
  unsigned = bitcast_convert_type(x, unsigned_dtype)

  # We cannot standardize zeros in x because XLA elides this is some cases.
  # We cannot standardize NaNs in x because it triggers jax.debug_nans
  # So instead we do these replacements in the signed integer representation.

  # Standardize zeros:
  signed = select(eq(x, _zero(x)), _zeros(signed), signed)
  # Standardize nans:
  signed_nan = x.dtype.type(np.nan).view(signed_dtype)
  signed = select(_isnan(x), full_like(signed, signed_nan), signed)

  flipped = bitcast_convert_type(
    sub(unsigned_dtype.type(np.iinfo(signed_dtype).max), unsigned), signed_dtype)
  return select(lt(signed, _zero(signed)), flipped, signed)
