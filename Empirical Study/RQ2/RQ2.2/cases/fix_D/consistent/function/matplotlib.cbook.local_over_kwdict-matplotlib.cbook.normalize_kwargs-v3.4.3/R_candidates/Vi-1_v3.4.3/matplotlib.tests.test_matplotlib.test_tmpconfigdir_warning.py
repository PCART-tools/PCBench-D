@pytest.mark.skipif(
    os.name == "nt", reason="chmod() doesn't work as is on Windows")
@pytest.mark.skipif(os.name != "nt" and os.geteuid() == 0,
                    reason="chmod() doesn't work as root")
def test_tmpconfigdir_warning(tmpdir):
    """Test that a warning is emitted if a temporary configdir must be used."""
    mode = os.stat(tmpdir).st_mode
    try:
        os.chmod(tmpdir, 0)
        proc = subprocess.run(
            [sys.executable, "-c", "import matplotlib"],
            env={**os.environ, "MPLCONFIGDIR": str(tmpdir)},
            stderr=subprocess.PIPE, universal_newlines=True, check=True)
        assert "set the MPLCONFIGDIR" in proc.stderr
    finally:
        os.chmod(tmpdir, mode)
