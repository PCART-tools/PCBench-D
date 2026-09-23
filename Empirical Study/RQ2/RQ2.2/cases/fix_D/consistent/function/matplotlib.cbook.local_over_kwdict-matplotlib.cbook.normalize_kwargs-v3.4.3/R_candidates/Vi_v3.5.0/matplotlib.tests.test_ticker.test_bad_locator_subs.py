@pytest.mark.parametrize('sub', [
    ['hi', 'aardvark'],
    np.zeros((2, 2))])
def test_bad_locator_subs(sub):
    ll = mticker.LogLocator()
    with pytest.raises(ValueError):
        ll.subs(sub)
