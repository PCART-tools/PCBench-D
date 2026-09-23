def check_vonmises_cdf_periodic(k,l,s,x):
    vm = stats.vonmises(k,loc=l,scale=s)
    assert_almost_equal(vm.cdf(x) % 1,vm.cdf(x % (2*numpy.pi*s)) % 1)
