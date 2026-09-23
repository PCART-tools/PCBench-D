@contextlib.contextmanager
def profile():
    try:
        start()
        yield
    finally:
        stop()
