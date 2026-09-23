def test_use_url(tmpdir):
    path = Path(tmpdir, 'file')
    path.write_text('axes.facecolor: adeade')
    with temp_style('test', DUMMY_SETTINGS):
        url = ('file:'
               + ('///' if sys.platform == 'win32' else '')
               + path.resolve().as_posix())
        with style.context(url):
            assert mpl.rcParams['axes.facecolor'] == "#adeade"
