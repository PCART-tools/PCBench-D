@pytest.mark.skipif(sys.platform == 'win32',
                    reason='No other signal available to send on Windows')
@pytest.mark.backend('QtAgg', skip_on_importerror=True)
@pytest.mark.parametrize("target, kwargs", [
    ('show', {'block': True}),
    ('pause', {'interval': 10})
])
def test_other_signal_before_sigint(target, kwargs):
    backend = plt.get_backend()
    proc = WaitForStringPopen(
        [sys.executable, "-c",
         inspect.getsource(_test_other_signal_before_sigint_impl) +
         "\n_test_other_signal_before_sigint_impl("
            f"{backend!r}, {target!r}, {kwargs!r})"])
    try:
        proc.wait_for('DRAW')
        os.kill(proc.pid, signal.SIGUSR1)
        proc.wait_for('SIGUSR1')
        os.kill(proc.pid, signal.SIGINT)
        stdout, _ = proc.communicate(timeout=_test_timeout)
    except:
        proc.kill()
        stdout, _ = proc.communicate()
        raise
    print(stdout)
    assert 'SUCCESS' in stdout
    plt.figure()
