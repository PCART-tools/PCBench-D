def _convert_elt_type_folding_rule(consts, eqn):
  # We constant-fold convert_element_types applied to constants if those
  # constants are Python builtin numeric types or numpy.ndarrays (so as not
  # to perform any device operations when constant-folding) and if the output
  # type can be faithfully represented by a Python builtin numeric type or
  # numpy.ndarray. If those conditions are met, we output a numpy.ndarray
  # constant if the output type is not weak, and if the output type is weak then
  # we output a Python builtin numeric type.
  # TODO(mattjj): allow constant-folding CPU-backed JAX arrays
  c, = consts
  o, = eqn.outvars
  if (type(c) in {np.ndarray, *dtypes.python_scalar_dtypes} and
      isinstance(o.aval, core.UnshapedArray) and not np.shape(c)):
    out = np.array(c, eqn.params['new_dtype'])
    if not o.aval.weak_type:
      return [out], None
    out = out.item()
    if core.get_aval(out).dtype is o.aval.dtype:
      return [out], None
  return [None], eqn
