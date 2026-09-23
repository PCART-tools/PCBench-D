@pytest.mark.parametrize("env", _thread_safe_backends)
@pytest.mark.flaky(reruns=3)
def test_interactive_thread_safety(env):
    proc = subprocess.run(
        [sys.executable, "-c",
         inspect.getsource(_test_thread_impl) + "\n_test_thread_impl()"],
        env={**os.environ, "SOURCE_DATE_EPOCH": "0", **env},
        timeout=_test_timeout, check=True,
        stdout=subprocess.PIPE, universal_newlines=True)
    assert proc.stdout.count("CloseEvent") == 1
