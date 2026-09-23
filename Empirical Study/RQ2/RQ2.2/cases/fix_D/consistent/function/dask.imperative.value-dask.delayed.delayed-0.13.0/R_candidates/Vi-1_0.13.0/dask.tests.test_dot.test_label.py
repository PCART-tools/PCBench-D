def test_label():
    assert label('x') == 'x'
    assert label('elemwise-ffcd9aa2231d466b5aa91e8bfa9e9487') == 'elemwise-#'

    cache = {}
    result = label('elemwise-ffcd9aa2231d466b5aa91e8bfa9e9487', cache=cache)
    assert result == 'elemwise-#0'
    # cached
    result = label('elemwise-ffcd9aa2231d466b5aa91e8bfa9e9487', cache=cache)
    assert result == 'elemwise-#0'
    assert len(cache) == 1

    result = label('elemwise-e890b510984f344edea9a5e5fe05c0db', cache=cache)
    assert result == 'elemwise-#1'
    assert len(cache) == 2

    result = label('elemwise-ffcd9aa2231d466b5aa91e8bfa9e9487', cache=cache)
    assert result == 'elemwise-#0'
    assert len(cache) == 2

    assert label('x', cache=cache) == 'x'
    assert len(cache) == 2
