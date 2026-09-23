@pytest.mark.skipif(LooseVersion(np.__version__) < '1.14.0',
                    reason="NumPy doesn't have `np.linalg._umath_linalg` yet")
@pytest.mark.xfail(reason="Protect from `np.linalg._umath_linalg.eig` breaking")
def test_Array_numpy_gufunc_call__array_ufunc__02():
    x = da.random.normal(size=(3, 10, 10), chunks=(2, 10, 10))
    nx = x.compute()
    nw, nv = np.linalg._umath_linalg.eig(nx)
    w, v = np.linalg._umath_linalg.eig(x, output_dtypes=(float, float))
    vw = w.compute()
    vv = v.compute()
    assert_eq(nw, vw)
    assert_eq(nv, vv)
