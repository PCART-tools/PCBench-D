def _test_binary_broadcast(name, ref, filter_=None,
                           gcs=hu.gcs, allow_inplace=False, dtypes=_dtypes):
    @given(
        inputs=dtypes().flatmap(lambda dtype: _tensor_and_prefix(
            dtype=dtype,
            elements=hu.elements_of_type(dtype, filter_=filter_))),
        in_place=(st.booleans() if allow_inplace else st.just(False)),
        **gcs)
    @settings(max_examples=3, deadline=100)
    def test_binary_broadcast(self, inputs, in_place, gc, dc):
        op = core.CreateOperator(
            name, ["X1", "X2"], ["X1" if in_place else "Y"], broadcast=1)
        X1, X2 = inputs
        self.assertDeviceChecks(dc, op, [X1, X2], [0])

        def cast_ref(x, y):
            return (np.array(ref(x, y)[0], dtype=x.dtype), )

        # gradient not implemented yet
        # self.assertGradientChecks(gc, op, [X1, X2], 0, [0])
        self.assertReferenceChecks(gc, op, [X1, X2], cast_ref)

    return test_binary_broadcast
