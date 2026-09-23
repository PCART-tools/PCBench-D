def naryop_dtype_rule(result_dtype, accepted_dtypes, name, *avals, **kwargs):
  aval_dtypes = [aval.dtype for aval in avals]
  for i, (aval_dtype, types) in enumerate(zip(aval_dtypes, accepted_dtypes)):
    if not any(dtypes.issubdtype(aval_dtype, t) for t in types):
      if aval_dtype == dtypes.float0:
        raise TypeError(
            f"Called {name} with a float0 at position {i}. "
            "float0s do not support any operations by design, because they "
            "are not compatible with non-trivial vector spaces. No implicit dtype "
            "conversion is done. You can use np.zeros_like(arr, dtype=np.float) "
            "to cast a float0 array to a regular zeros array. \n"
            "If you didn't expect to get a float0 you might have accidentally "
            "taken a gradient with respect to an integer argument.")
      else:
        msg = ('{} does not accept dtype {} at position {}. '
               'Accepted dtypes at position {} are subtypes of {}.')
        typename = str(np.dtype(aval_dtype).name)
        typenames = ', '.join(t.__name__ for t in types)
        raise TypeError(msg.format(name, typename, i, i, typenames))
  _check_same_dtypes(name, False, *aval_dtypes)
  return result_dtype(*avals)
