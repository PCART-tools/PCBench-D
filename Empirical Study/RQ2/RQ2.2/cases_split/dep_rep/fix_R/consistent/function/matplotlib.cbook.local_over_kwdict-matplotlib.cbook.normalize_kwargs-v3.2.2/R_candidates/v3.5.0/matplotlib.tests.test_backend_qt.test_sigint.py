@pytest.mark.backend('QtAgg', skip_on_importerror=True)
@pytest.mark.parametrize("target, kwargs", [
    ('show', {'block': True}),
    ('pause', {'interval': 10})
])
def test_sigint(target, kwargs):
    backend = plt.get_backend()
    proc = WaitForStringPopen(
        [sys.executable, "-c",
         inspect.getsource(_test_sigint_impl) +
         f"\n_test_sigint_impl({backend!r}, {target!r}, {kwargs!r})"])
    try:
        proc.wait_for('DRAW')
        stdout, _ = proc.communicate(timeout=_test_timeout)
    except:
        proc.kill()
        stdout, _ = proc.communicate()
        raise
    print(stdout)
    assert 'SUCCESS' in stdout
