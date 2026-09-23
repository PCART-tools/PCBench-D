def test_progressbar(capsys):
    with ProgressBar():
        out = get(dsk, 'e')
    assert out == 6
    check_bar_completed(capsys)
    with ProgressBar(width=20):
        out = get(dsk, 'e')
    check_bar_completed(capsys, 20)
