@contextmanager
def ignoring(*exceptions):
    try:
        yield
    except exceptions:
        pass
