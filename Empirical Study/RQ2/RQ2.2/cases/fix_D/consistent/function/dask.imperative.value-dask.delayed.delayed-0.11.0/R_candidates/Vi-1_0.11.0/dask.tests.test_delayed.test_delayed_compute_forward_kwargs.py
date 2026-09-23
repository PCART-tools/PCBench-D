def test_delayed_compute_forward_kwargs():
    x = delayed(1) + 2
    x.compute(bogus_keyword=10)
