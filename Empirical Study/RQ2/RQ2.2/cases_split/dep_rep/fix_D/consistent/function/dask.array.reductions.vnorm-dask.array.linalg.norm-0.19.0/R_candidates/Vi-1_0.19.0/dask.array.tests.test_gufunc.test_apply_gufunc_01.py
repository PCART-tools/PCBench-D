def test_apply_gufunc_01():
    def stats(x):
        return np.mean(x, axis=-1), np.std(x, axis=-1)
    a = da.random.normal(size=(10, 20, 30), chunks=(5, 5, 30))
    mean, std = apply_gufunc(stats, "(i)->(),()", a,
                             output_dtypes=2 * (a.dtype,))
    assert mean.compute().shape == (10, 20)
    assert std.compute().shape == (10, 20)
