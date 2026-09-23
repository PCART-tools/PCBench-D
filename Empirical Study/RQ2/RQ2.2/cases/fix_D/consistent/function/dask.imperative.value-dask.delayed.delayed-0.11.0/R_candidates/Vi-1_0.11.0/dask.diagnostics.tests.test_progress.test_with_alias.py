def test_with_alias(capsys):
    dsk = {'a': 1,
           'b': 2,
           'c': (add, 'a', 'b'),
           'd': (add, 1, 2),
           'e': 'd',
           'f': (mul, 'e', 'c')}
    with ProgressBar():
        get(dsk, 'f')
    check_bar_completed(capsys)
