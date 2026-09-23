@_wraps(scipy.linalg.lu, update_doc=False,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'check_finite'))
@partial(jit, static_argnames=('permute_l', 'overwrite_a', 'check_finite'))
def lu(a, permute_l=False, overwrite_a=False, check_finite=True):
  del overwrite_a, check_finite
  return _lu(a, permute_l)
