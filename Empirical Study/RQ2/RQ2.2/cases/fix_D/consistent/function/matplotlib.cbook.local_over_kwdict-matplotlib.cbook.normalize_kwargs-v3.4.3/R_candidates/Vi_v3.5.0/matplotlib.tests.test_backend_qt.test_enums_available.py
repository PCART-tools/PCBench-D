@pytest.mark.parametrize("env", _get_testable_qt_backends())
def test_enums_available(env):
    proc = subprocess.run(
        [sys.executable, "-c",
         inspect.getsource(_test_enums_impl) + "\n_test_enums_impl()"],
        env={**os.environ, "SOURCE_DATE_EPOCH": "0", **env},
        timeout=_test_timeout, check=True,
        stdout=subprocess.PIPE, universal_newlines=True)
