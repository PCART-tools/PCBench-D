@pytest.mark.parametrize('a', [np.arange(11),
                               np.arange(6).reshape((3,2))
                               ])
@pytest.mark.parametrize('returned', [True, False])
def test_average(a, returned):
    d_a = da.from_array(a, chunks=2)

    np_avg = np.average(a, returned=returned)
    da_avg = da.average(d_a, returned=returned)

    assert_eq(np_avg, da_avg)
