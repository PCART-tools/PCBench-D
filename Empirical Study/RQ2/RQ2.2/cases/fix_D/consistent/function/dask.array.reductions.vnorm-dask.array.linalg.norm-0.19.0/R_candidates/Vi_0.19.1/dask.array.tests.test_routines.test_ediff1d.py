@pytest.mark.parametrize('shape', [
    (10,),
    (10, 15),
])
@pytest.mark.parametrize('to_end, to_begin', [
    [None, None],
    [0, 0],
    [[1, 2], [3, 4]],
])
def test_ediff1d(shape, to_end, to_begin):
    x = np.random.randint(0, 10, shape)
    a = da.from_array(x, chunks=(len(shape) * (5,)))

    assert_eq(da.ediff1d(a, to_end, to_begin), np.ediff1d(x, to_end, to_begin))
