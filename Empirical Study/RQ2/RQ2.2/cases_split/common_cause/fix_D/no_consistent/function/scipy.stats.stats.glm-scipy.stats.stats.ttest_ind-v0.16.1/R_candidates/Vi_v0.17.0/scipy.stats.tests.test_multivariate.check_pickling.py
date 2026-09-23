def check_pickling(distfn, args):
    # check that a distribution instance pickles and unpickles
    # pay special attention to the random_state property

    # save the random_state (restore later)
    rndm = distfn.random_state

    distfn.random_state = 1234
    distfn.rvs(*args, size=8)
    s = pickle.dumps(distfn)
    r0 = distfn.rvs(*args, size=8)

    unpickled = pickle.loads(s)
    r1 = unpickled.rvs(*args, size=8)
    assert_equal(r0, r1)

    # restore the random_state
    distfn.random_state = rndm
