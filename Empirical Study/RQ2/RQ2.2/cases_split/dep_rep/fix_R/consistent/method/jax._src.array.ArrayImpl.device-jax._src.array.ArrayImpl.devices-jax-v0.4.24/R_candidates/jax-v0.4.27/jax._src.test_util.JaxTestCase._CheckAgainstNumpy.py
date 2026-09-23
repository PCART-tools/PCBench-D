  def _CheckAgainstNumpy(self, numpy_reference_op, lax_op, args_maker,
                         check_dtypes=True, tol=None, atol=None, rtol=None,
                         canonicalize_dtypes=True):
    args = args_maker()
    lax_ans = lax_op(*args)
    numpy_ans = numpy_reference_op(*args)
    self.assertAllClose(numpy_ans, lax_ans, check_dtypes=check_dtypes,
                        atol=atol or tol, rtol=rtol or tol,
                        canonicalize_dtypes=canonicalize_dtypes)
