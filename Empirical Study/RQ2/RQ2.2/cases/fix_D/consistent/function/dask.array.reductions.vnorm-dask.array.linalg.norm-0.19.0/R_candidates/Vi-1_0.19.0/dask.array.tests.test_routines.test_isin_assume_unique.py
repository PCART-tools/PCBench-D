@pytest.mark.parametrize("assume_unique", [True, False])
@pytest.mark.skipif(LooseVersion(np.__version__) < '1.13.0',
                    reason="np.isin is new in numpy 1.13")
def test_isin_assume_unique(assume_unique):
    a1 = np.arange(10)
    d1 = da.from_array(a1, chunks=(5,))

    test_elements = np.arange(0, 10, 2)
    r_a = np.isin(a1, test_elements, assume_unique=assume_unique)
    r_d = da.isin(d1, test_elements, assume_unique=assume_unique)
    assert_eq(r_a, r_d)
