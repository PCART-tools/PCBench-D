@pytest.mark.parametrize('shape, chunks', [
    ((10,), (1,)),
    ((10, 11, 13), (4, 5, 3)),
])
@pytest.mark.parametrize('reps', [0, 1, 2, 3, 5])
def test_tile(shape, chunks, reps):
    x = np.random.random(shape)
    d = da.from_array(x, chunks=chunks)

    assert_eq(np.tile(x, reps), da.tile(d, reps))
