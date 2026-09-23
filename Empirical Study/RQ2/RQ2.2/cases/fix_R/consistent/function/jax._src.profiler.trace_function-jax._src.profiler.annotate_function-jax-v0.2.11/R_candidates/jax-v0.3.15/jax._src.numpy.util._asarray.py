def _asarray(arr):
  """
  Pared-down utility to convert object to a DeviceArray.
  Note this will not correctly handle lists or tuples.
  """
  _check_arraylike("_asarray", arr)
  dtype, weak_type = dtypes._lattice_result_type(arr)
  return lax_internal._convert_element_type(arr, dtype, weak_type)
