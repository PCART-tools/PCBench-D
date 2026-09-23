@pytest.mark.parametrize(
    "method_name",
    [pytest.param("to_html5_video", marks=pytest.mark.skipif(
        not animation.writers.is_available(mpl.rcParams["animation.writer"]),
        reason="animation writer not installed")),
     "to_jshtml"])
@pytest.mark.parametrize('anim', [dict(frames=1)], indirect=['anim'])
def test_cleanup_temporaries(method_name, tmpdir, anim):
    with tmpdir.as_cwd():
        getattr(anim, method_name)()
        assert list(Path(str(tmpdir)).iterdir()) == []
