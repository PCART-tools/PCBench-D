def test_unpicklable_results_generate_errors():

    dsk = {'x': (make_bad_result,)}

    try:
        get(dsk, 'x')
    except Exception as e:
        # can't use type because pickle / cPickle distinction
        assert type(e).__name__ in ('PicklingError', 'AttributeError')
