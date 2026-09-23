def test_where_incorrect_args():
    a = da.ones(5, chunks=3)

    for kwd in ["x", "y"]:
        kwargs = {kwd: a}
        try:
            da.where(a > 0, **kwargs)
        except ValueError as e:
            assert 'either both or neither of x and y should be given' in str(e)
