@pytest.mark.parametrize(
    "args",
    [(np.arange(12).reshape(3, 4), 'a'),
     (np.arange(12), 'a'),
     (np.arange(12), np.arange(3))])
def test_step_fails(args):
    with pytest.raises(ValueError):
        cbook.pts_to_prestep(*args)
