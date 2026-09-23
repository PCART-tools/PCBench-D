@pytest.mark.quality
def test_flake8():
    pytest.importorskip('flake8')

    chdir(TOP_PATH)

    proc = Popen(["flake8", "dask"], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()

    assert proc.returncode == 0, "Flake8 issues:\n%s" % out.decode("utf-8")
