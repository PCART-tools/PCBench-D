def test_vonmises_numerical():
    vm = stats.vonmises(800)
    assert_almost_equal(vm.cdf(0), 0.5)
