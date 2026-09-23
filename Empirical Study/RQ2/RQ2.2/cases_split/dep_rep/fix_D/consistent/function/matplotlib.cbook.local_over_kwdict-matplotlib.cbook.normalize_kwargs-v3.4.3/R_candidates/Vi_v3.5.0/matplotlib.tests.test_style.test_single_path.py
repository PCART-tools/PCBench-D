def test_single_path(tmpdir):
    mpl.rcParams[PARAM] = 'gray'
    temp_file = f'text.{STYLE_EXTENSION}'
    path = Path(tmpdir, temp_file)
    path.write_text(f'{PARAM} : {VALUE}')
    with style.context(path):
        assert mpl.rcParams[PARAM] == VALUE
    assert mpl.rcParams[PARAM] == 'gray'
