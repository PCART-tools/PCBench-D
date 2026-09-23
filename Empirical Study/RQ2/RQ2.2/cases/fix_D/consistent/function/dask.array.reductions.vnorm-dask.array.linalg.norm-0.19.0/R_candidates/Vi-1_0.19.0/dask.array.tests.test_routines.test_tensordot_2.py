@pytest.mark.parametrize('axes', [
    0,
    1,
    (0, 1),
    (1, 0),
    ((1, 0), (2, 1)),
    ((1, 2), (2, 0)),
    ((2, 0), (1, 2))
])
def test_tensordot_2(axes):
    x = np.arange(4 * 4 * 4).reshape((4, 4, 4))
    y = da.from_array(x, chunks=2)

    assert_eq(da.tensordot(y, y, axes=axes),
              np.tensordot(x, x, axes=axes))
