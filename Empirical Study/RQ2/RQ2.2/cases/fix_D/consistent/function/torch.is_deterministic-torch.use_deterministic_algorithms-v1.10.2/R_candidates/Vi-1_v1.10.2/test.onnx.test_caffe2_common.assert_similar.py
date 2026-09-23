def assert_similar(ref, real):
    np.testing.assert_equal(len(ref), len(real))
    for i in range(len(ref)):
        np.testing.assert_allclose(ref[i], real[i], rtol=1e-3)
