def test_errors_propagate():
    dsk = {'x': (bad,)}

    try:
        get(dsk, 'x')
    except Exception as e:
        assert isinstance(e, ValueError)
        assert "12345" in str(e)
