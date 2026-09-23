@dec.skipif(not _test_round.have_fenv())
def test_add_round_up():
    np.random.seed(1234)
    _test_round.test_add_round(10**5, 'up')
