@pytest.mark.skipif(LooseVersion(np.__version__) < '1.13.0',
                    reason="NumPy doesn't support `block` yet")
def test_block_mixed_1d_and_2d():
    a1 = np.ones((2, 2))
    a2 = np.array([2, 2])

    d1 = da.asarray(a1)
    d2 = da.asarray(a2)

    expected = np.block([[d1], [d2]])
    result = da.block([[a1], [a2]])

    assert_eq(expected, result)
