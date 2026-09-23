def test_exception_all_func(i):
    time.sleep(random.random() / 10)
    raise ValueError("legitimate exception from process %d" % i)
