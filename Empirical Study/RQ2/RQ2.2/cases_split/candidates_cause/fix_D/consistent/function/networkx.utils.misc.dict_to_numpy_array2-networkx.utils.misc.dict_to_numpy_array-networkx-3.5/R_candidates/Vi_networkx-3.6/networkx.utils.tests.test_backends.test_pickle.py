def test_pickle():
    count = 0
    for name, func in nx.utils.backends._registered_algorithms.items():
        pickled = pickle.dumps(func.__wrapped__)
        assert pickle.loads(pickled) is func.__wrapped__
        try:
            # Some functions can't be pickled, but it's not b/c of _dispatchable
            pickled = pickle.dumps(func)
        except pickle.PicklingError:
            continue
        assert pickle.loads(pickled) is func
        count += 1
    assert count > 0
    assert pickle.loads(pickle.dumps(nx.inverse_line_graph)) is nx.inverse_line_graph
