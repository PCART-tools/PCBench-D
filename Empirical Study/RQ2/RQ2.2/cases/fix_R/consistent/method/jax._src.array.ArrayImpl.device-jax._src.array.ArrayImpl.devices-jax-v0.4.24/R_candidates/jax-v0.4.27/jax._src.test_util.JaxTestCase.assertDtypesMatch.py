  def assertDtypesMatch(self, x, y, *, canonicalize_dtypes=True):
    if not config.enable_x64.value and canonicalize_dtypes:
      self.assertEqual(_dtypes.canonicalize_dtype(_dtype(x), allow_extended_dtype=True),
                       _dtypes.canonicalize_dtype(_dtype(y), allow_extended_dtype=True))
    else:
      self.assertEqual(_dtype(x), _dtype(y))
