def test_skip_doctest():
    example = """>>> xxx
>>>
>>> # comment
>>> xxx"""

    res = skip_doctest(example)
    assert res == """>>> xxx    # doctest: +SKIP
>>>
>>> # comment
>>> xxx    # doctest: +SKIP"""

    assert skip_doctest(None) == ''
