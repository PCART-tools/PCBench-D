@pytest.mark.skipif(LooseVersion(np.__version__) < '1.13.0',
                    reason="NumPy doesn't support `block` yet")
def test_block_3d():
    a000 = np.ones((2, 2, 2), int) * 1

    a100 = np.ones((3, 2, 2), int) * 2
    a010 = np.ones((2, 3, 2), int) * 3
    a001 = np.ones((2, 2, 3), int) * 4

    a011 = np.ones((2, 3, 3), int) * 5
    a101 = np.ones((3, 2, 3), int) * 6
    a110 = np.ones((3, 3, 2), int) * 7

    a111 = np.ones((3, 3, 3), int) * 8

    d000 = da.asarray(a000)

    d100 = da.asarray(a100)
    d010 = da.asarray(a010)
    d001 = da.asarray(a001)

    d011 = da.asarray(a011)
    d101 = da.asarray(a101)
    d110 = da.asarray(a110)

    d111 = da.asarray(a111)

    expected = np.block([
        [
            [a000, a001],
            [a010, a011],
        ],
        [
            [a100, a101],
            [a110, a111],
        ]
    ])
    result = da.block([
        [
            [d000, d001],
            [d010, d011],
        ],
        [
            [d100, d101],
            [d110, d111],
        ]
    ])

    assert_eq(expected, result)
