@pytest.mark.parametrize('shape, chunks', [
    ((10,), (1,)),
    ((10, 11, 13), (4, 5, 3)),
])
@pytest.mark.parametrize('reps', [[1], [1, 2]])
def test_tile_array_reps(shape, chunks, reps):
    x = np.random.random(shape)
    d = da.from_array(x, chunks=chunks)

    with pytest.raises(NotImplementedError):
        da.tile(d, reps)
