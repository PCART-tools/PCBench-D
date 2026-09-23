@pytest.mark.skipif(LooseVersion(np.__version__) < '1.12.0',
                    reason="`np.vectorize(..., signature=...)` not supported yet")
@pytest.mark.parametrize('vectorize', [False, True])
def test_apply_gufunc_output_dtypes_string(vectorize):
    def stats(x):
        return np.mean(x, axis=-1)
    a = da.random.normal(size=(10, 20, 30), chunks=(5, 5, 30))
    mean = apply_gufunc(stats, "(i)->()", a, output_dtypes="f", vectorize=vectorize)
    assert mean.compute().shape == (10, 20)
