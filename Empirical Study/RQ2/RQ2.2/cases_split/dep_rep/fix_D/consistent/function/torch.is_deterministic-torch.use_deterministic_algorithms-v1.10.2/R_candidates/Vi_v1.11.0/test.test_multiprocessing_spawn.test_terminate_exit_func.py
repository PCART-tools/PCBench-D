def test_terminate_exit_func(i, arg):
    if i == 0:
        sys.exit(arg)
    time.sleep(1.0)
