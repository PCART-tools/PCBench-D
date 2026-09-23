def test_success_first_then_exception_func(i, arg):
    if i == 0:
        return
    time.sleep(0.1)
    raise ValueError("legitimate exception")
