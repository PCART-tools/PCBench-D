@pytest.mark.style('default')
def test_capstyle():
    col = mcollections.PathCollection([], capstyle='round')
    assert col.get_capstyle() == 'round'
    col.set_capstyle('butt')
    assert col.get_capstyle() == 'butt'
