@pytest.mark.parametrize('kind', ('over', 'under', 'bad'))
def test_non_mutable_get_values(kind):
    cmap = copy.copy(plt.get_cmap('viridis'))
    init_value = getattr(cmap, f'get_{kind}')()
    getattr(cmap, f'set_{kind}')('k')
    black_value = getattr(cmap, f'get_{kind}')()
    assert np.all(black_value == [0, 0, 0, 1])
    assert not np.all(init_value == black_value)
