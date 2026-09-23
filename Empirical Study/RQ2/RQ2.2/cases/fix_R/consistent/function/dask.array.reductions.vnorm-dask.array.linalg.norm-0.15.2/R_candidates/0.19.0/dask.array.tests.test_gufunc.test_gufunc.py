@pytest.mark.skipif(LooseVersion(np.__version__) < '1.12.0',
                    reason="`np.vectorize(..., signature=...)` not supported yet")
def test_gufunc():
    x = da.random.normal(size=(10, 5), chunks=(2, 5))

    def foo(x):
        return np.mean(x, axis=-1)
    gufoo = gufunc(foo, signature="(i)->()", output_dtypes=float, vectorize=True)

    y = gufoo(x)
    valy = y.compute()
    assert isinstance(y, Array)
    assert valy.shape == (10,)
