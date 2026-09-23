def test_clean_exit():
    dsk = {'a': (lambda: 1 / 0, )}
    try:
        with ProgressBar() as pbar:
            get(dsk, 'a')
    except ZeroDivisionError:
        pass
    assert not pbar._running
    assert not pbar._timer.is_alive()
