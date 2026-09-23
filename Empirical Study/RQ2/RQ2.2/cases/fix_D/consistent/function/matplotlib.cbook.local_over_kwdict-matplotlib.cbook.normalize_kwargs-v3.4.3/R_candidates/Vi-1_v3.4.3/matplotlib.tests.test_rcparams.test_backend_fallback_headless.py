@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
def test_backend_fallback_headless(tmpdir):
    env = {**os.environ,
           "DISPLAY": "", "WAYLAND_DISPLAY": "",
           "MPLBACKEND": "", "MPLCONFIGDIR": str(tmpdir)}
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run(
            [sys.executable, "-c",
             ("import matplotlib;" +
              "matplotlib.use('tkagg');" +
              "import matplotlib.pyplot")
             ],
            env=env, check=True)
