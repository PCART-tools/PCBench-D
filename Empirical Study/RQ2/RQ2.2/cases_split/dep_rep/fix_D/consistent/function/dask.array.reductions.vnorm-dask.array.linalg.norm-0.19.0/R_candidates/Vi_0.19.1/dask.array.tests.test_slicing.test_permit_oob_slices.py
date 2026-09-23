def test_permit_oob_slices():
    x = np.arange(5)
    dx = da.from_array(x, chunks=2)

    assert_eq(x[-102:], dx[-102:])
    assert_eq(x[102:], dx[102:])
    assert_eq(x[:102], dx[:102])
    assert_eq(x[:-102], dx[:-102])
