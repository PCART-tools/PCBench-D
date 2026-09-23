def test_register(capsys):
    try:
        p = ProgressBar()
        p.register()

        assert _globals['callbacks']

        get(dsk, 'e')
        check_bar_completed(capsys)

        p.unregister()

        assert not _globals['callbacks']
    finally:
        _globals['callbacks'].clear()
