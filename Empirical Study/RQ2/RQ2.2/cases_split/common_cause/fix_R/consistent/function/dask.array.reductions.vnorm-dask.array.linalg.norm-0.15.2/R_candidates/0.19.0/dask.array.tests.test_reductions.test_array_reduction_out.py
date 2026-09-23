@pytest.mark.skipif(np.__version__ < '1.12.0', reason='argmax out parameter')
@pytest.mark.parametrize('func', [np.sum,
                                  np.argmax])
def test_array_reduction_out(func):
    x = da.arange(10, chunks=(5,))
    y = da.ones((10, 10), chunks=(4, 4))
    func(y, axis=0, out=x)
    assert_eq(x, func(np.ones((10, 10)), axis=0))
