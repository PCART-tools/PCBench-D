@pytest.mark.parametrize("env", _get_testable_interactive_backends())
@pytest.mark.parametrize("toolbar", ["toolbar2", "toolmanager"])
@pytest.mark.flaky(reruns=3)
def test_interactive_backend(env, toolbar):
    if env["MPLBACKEND"] == "macosx":
        if toolbar == "toolmanager":
            pytest.skip("toolmanager is not implemented for macosx.")

    proc = subprocess.run(
        [sys.executable, "-c",
         inspect.getsource(_test_interactive_impl)
         + "\n_test_interactive_impl()",
         json.dumps({"toolbar": toolbar})],
        env={**os.environ, "SOURCE_DATE_EPOCH": "0", **env},
        timeout=_test_timeout,
        stdout=subprocess.PIPE, universal_newlines=True)
    if proc.returncode:
        pytest.fail("The subprocess returned with non-zero exit status "
                    f"{proc.returncode}.")
    assert proc.stdout.count("CloseEvent") == 1
