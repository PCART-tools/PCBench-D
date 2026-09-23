def test_minimum_time(capsys):
    with ProgressBar(1.0):
        out = get(dsk, 'e')
    out, err = capsys.readouterr()
    assert out == '' and err == ''
