@pytest.mark.skipif(not has_fclist, reason='no fontconfig installed')
def test_get_fontconfig_fonts():
    assert len(get_fontconfig_fonts()) > 1
