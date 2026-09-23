@pytest.mark.skipif(
    sys.platform == "linux" and not _c_internal_utils.display_is_valid(),
    reason="headless")
def test_backend_fallback_headful(tmpdir):
    pytest.importorskip("tkinter")
    env = {**os.environ, "MPLBACKEND": "", "MPLCONFIGDIR": str(tmpdir)}
    backend = subprocess.check_output(
        [sys.executable, "-c",
         "import matplotlib.pyplot; print(matplotlib.get_backend())"],
        env=env, universal_newlines=True)
    # The actual backend will depend on what's installed, but at least tkagg is
    # present.
    assert backend.strip().lower() != "agg"
