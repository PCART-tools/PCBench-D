def test_unpicklable_args_generate_errors():
    a = NotUnpickleable()

    def foo(a):
        return 1

    dsk = {'x': (foo, a)}

    try:
        get(dsk, 'x')
    except Exception as e:
        assert isinstance(e, ValueError)

    dsk = {'x': (foo, 'a'),
           'a': a}

    try:
        get(dsk, 'x')
    except Exception as e:
        assert isinstance(e, ValueError)
