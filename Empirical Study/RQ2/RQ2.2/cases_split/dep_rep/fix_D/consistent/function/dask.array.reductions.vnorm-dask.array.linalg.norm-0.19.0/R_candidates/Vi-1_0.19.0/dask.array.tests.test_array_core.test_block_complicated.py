@pytest.mark.skipif(LooseVersion(np.__version__) < '1.13.0',
                    reason="NumPy doesn't support `block` yet")
def test_block_complicated():
    # a bit more complicated
    a1 = np.array([[1, 1, 1]])
    a2 = np.array([[2, 2, 2]])
    a3 = np.array([[3, 3, 3, 3, 3, 3]])
    a4 = np.array([4, 4, 4, 4, 4, 4])
    a5 = np.array(5)
    a6 = np.array([6, 6, 6, 6, 6])
    a7 = np.zeros((2, 6))

    d1 = da.asarray(a1)
    d2 = da.asarray(a2)
    d3 = da.asarray(a3)
    d4 = da.asarray(a4)
    d5 = da.asarray(a5)
    d6 = da.asarray(a6)
    d7 = da.asarray(a7)

    expected = np.block([[a1, a2],
                         [a3],
                         [a4],
                         [a5, a6],
                         [a7]])
    result = da.block([[d1, d2],
                       [d3],
                       [d4],
                       [d5, d6],
                       [d7]])

    assert_eq(expected, result)
