def expect_tensor(scalar_type, shape=None):
    def verify(actual_type):
        np.testing.assert_equal(actual_type.scalarType(), scalar_type)
        # if shape is not None:
        #     np.testing.assert_equal(actual_type.sizes(), shape)
        if shape is not None:
            np.testing.assert_equal(actual_type.varyingSizes(), shape)
    return verify
