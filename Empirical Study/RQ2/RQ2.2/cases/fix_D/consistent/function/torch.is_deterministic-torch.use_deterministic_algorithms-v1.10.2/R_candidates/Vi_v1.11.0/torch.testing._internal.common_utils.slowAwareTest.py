def slowAwareTest(fn):
    fn.__dict__['slow_test'] = True
    return fn
