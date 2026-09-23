def _assert_numpy_allclose(a, b, atol=None, rtol=None, err_msg=''):
  if a.dtype == b.dtype == _dtypes.float0:
    np.testing.assert_array_equal(a, b, err_msg=err_msg)
    return
  if _fp8_enabled:
    custom_dtypes = [_dtypes.float8_e4m3fn, _dtypes.float8_e5m2, _dtypes.bfloat16]
  else:
    custom_dtypes = [_dtypes.bfloat16]
  a = a.astype(np.float32) if a.dtype in custom_dtypes else a
  b = b.astype(np.float32) if b.dtype in custom_dtypes else b
  kw = {}
  if atol: kw["atol"] = atol
  if rtol: kw["rtol"] = rtol
  with np.errstate(invalid='ignore'):
    # TODO(phawkins): surprisingly, assert_allclose sometimes reports invalid
    # value errors. It should not do that.
    np.testing.assert_allclose(a, b, **kw, err_msg=err_msg)
