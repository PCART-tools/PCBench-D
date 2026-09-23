def test_find_invalid(tmpdir):
    tmp_path = Path(tmpdir)

    with pytest.raises(FileNotFoundError):
        get_font(tmp_path / 'non-existent-font-name.ttf')

    with pytest.raises(FileNotFoundError):
        get_font(str(tmp_path / 'non-existent-font-name.ttf'))

    with pytest.raises(FileNotFoundError):
        get_font(bytes(tmp_path / 'non-existent-font-name.ttf'))

    # Not really public, but get_font doesn't expose non-filename constructor.
    from matplotlib.ft2font import FT2Font
    with pytest.raises(TypeError, match='path or binary-mode file'):
        FT2Font(StringIO())
