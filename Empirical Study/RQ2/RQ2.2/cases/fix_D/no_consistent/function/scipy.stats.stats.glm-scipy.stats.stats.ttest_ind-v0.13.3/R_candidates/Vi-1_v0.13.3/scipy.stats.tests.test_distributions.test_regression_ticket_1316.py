def test_regression_ticket_1316():
    # The following was raising an exception, because _construct_default_doc()
    # did not handle the default keyword extradoc=None.  See ticket #1316.
    g = stats.distributions.gamma_gen(name='gamma')
