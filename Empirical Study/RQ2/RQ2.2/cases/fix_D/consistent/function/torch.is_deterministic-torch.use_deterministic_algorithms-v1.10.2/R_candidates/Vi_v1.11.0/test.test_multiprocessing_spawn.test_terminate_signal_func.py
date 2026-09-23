def test_terminate_signal_func(i):
    if i == 0:
        os.kill(os.getpid(), signal.SIGABRT)
    time.sleep(1.0)
