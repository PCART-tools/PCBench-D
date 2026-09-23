@pytest.mark.parametrize('numticks', [1, 2, 3, 9])
@pytest.mark.style('default')
def test_small_range_loglocator(numticks):
    ll = mticker.LogLocator()
    ll.set_params(numticks=numticks)
    for top in [5, 7, 9, 11, 15, 50, 100, 1000]:
        ticks = ll.tick_values(.5, top)
        assert (np.diff(np.log10(ll.tick_values(6, 150))) == 1).all()
