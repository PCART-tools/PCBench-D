@pytest.mark.skipif(LooseVersion(np.__version__) < '1.13.0',
                    reason="NumPy doesn't support `block` yet")
def test_block_with_1d_arrays_multiple_rows():
    a1 = np.array([1, 2, 3])
    a2 = np.array([2, 3, 4])

    d1 = da.asarray(a1)
    d2 = da.asarray(a2)

    expected = np.block([[a1, a2], [a1, a2]])
    result = da.block([[d1, d2], [d1, d2]])

    assert_eq(expected, result)
