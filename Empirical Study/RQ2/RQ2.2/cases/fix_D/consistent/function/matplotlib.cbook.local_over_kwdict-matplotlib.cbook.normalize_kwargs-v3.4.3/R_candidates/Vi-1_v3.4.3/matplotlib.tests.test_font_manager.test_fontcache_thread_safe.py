def test_fontcache_thread_safe():
    pytest.importorskip('threading')
    import inspect

    proc = subprocess.run(
        [sys.executable, "-c",
         inspect.getsource(_test_threading) + '\n_test_threading()']
    )
    if proc.returncode:
        pytest.fail("The subprocess returned with non-zero exit status "
                    f"{proc.returncode}.")
