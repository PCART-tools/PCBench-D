def _test_binary(name, ref, filter_=None, gcs=hu.gcs,
                 test_gradient=False, allow_inplace=False, dtypes=_dtypes):
    @given(
        inputs=dtypes().flatmap(
            lambda dtype: hu.tensors(
                n=2, dtype=dtype,
                elements=hu.elements_of_type(dtype, filter_=filter_))),
        out=st.sampled_from(('Y', 'X1', 'X2') if allow_inplace else ('Y',)),
        **gcs)
    @settings(max_examples=20, deadline=None)
    def test_binary(self, inputs, out, gc, dc):
        op = core.CreateOperator(name, ["X1", "X2"], [out])
        X1, X2 = inputs
        self.assertDeviceChecks(dc, op, [X1, X2], [0])
        # We only do gradient check with float32 types.
        if test_gradient and X1.dtype == np.float32:
            self.assertGradientChecks(gc, op, [X1, X2], 0, [0])
        self.assertReferenceChecks(gc, op, [X1, X2], ref)

    return test_binary
