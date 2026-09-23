  def assertArraysEqual(self, x, y, *, check_dtypes=True, err_msg='',
                        allow_object_dtype=False, verbose=True):
    """Assert that x and y arrays are exactly equal."""
    if check_dtypes:
      self.assertDtypesMatch(x, y)
    x = np.asarray(x)
    y = np.asarray(y)

    if (not allow_object_dtype) and (x.dtype == object or y.dtype == object):
      # See https://github.com/google/jax/issues/17867
      raise TypeError(
        "assertArraysEqual may be poorly behaved when np.asarray casts to dtype=object. "
        "If comparing PRNG keys, consider random_test.KeyArrayTest.assertKeysEqual. "
        "If comparing collections of arrays, consider using assertAllClose. "
        "To let this test proceed anyway, pass allow_object_dtype=True.")

    # Work around https://github.com/numpy/numpy/issues/18992
    with np.errstate(over='ignore'):
      np.testing.assert_array_equal(x, y, err_msg=err_msg,
                                    verbose=verbose)
