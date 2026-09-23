def _assert_arrays_equal(actual, ref, err_msg):
    if ref.dtype.kind in ("S", "O", "U"):
        np.testing.assert_array_equal(actual, ref, err_msg=err_msg)
    else:
        np.testing.assert_allclose(actual, ref, atol=1e-4, rtol=1e-4, err_msg=err_msg)
