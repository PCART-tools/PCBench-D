def check_vonmises_pdf_periodic(k, l, s, x):
    vm = stats.vonmises(k, loc=l, scale=s)
    assert_almost_equal(vm.pdf(x), vm.pdf(x % (2*numpy.pi*s)))
