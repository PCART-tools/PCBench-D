@pytest.mark.skipif(LooseVersion(np.__version__) < '1.14.0',
                    reason="NumPy doesn't have `np.linalg._umath_linalg` yet")
@pytest.mark.xfail(reason="Protect from `np.linalg._umath_linalg.inv` breaking")
def test_Array_numpy_gufunc_call__array_ufunc__01():
    x = da.random.normal(size=(3, 10, 10), chunks=(2, 10, 10))
    nx = x.compute()
    ny = np.linalg._umath_linalg.inv(nx)
    y = np.linalg._umath_linalg.inv(x, output_dtypes=float)
    vy = y.compute()
    assert_eq(ny, vy)
