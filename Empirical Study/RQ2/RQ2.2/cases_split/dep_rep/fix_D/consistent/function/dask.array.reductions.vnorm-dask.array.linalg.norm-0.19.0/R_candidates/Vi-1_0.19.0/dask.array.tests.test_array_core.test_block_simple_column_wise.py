@pytest.mark.skipif(LooseVersion(np.__version__) < '1.13.0',
                    reason="NumPy doesn't support `block` yet")
def test_block_simple_column_wise():
    a1 = np.ones((2, 2))
    a2 = 2 * a1

    d1 = da.asarray(a1)
    d2 = da.asarray(a2)

    expected = np.block([[a1], [a2]])
    result = da.block([[d1], [d2]])

    assert_eq(expected, result)
