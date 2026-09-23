def test_exception_single_func(i, arg):
    if i == arg:
        raise ValueError("legitimate exception from process %d" % i)
    time.sleep(1.0)
