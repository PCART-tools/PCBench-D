@pytest.mark.parametrize('x,chunks', [
    (np.arange(25).reshape((5, 5)), (5, 5)),
    (np.arange(25).reshape((5, 5)), -1),
    (np.array([[1]]), 1),
    (np.array(1), 1),
])
def test_from_array_tasks_always_call_getter(x, chunks):
    dx = da.from_array(MyArray(x), chunks=chunks, asarray=False)
    assert_eq(x, dx)
