def test_no_tasks(capsys):
    with ProgressBar():
        get({'x': 1}, 'x')
    check_bar_completed(capsys)
