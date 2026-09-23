def debug(f):
    '''
    Use this method to decorate your function with DebugMode's functionality

    Example:

    @debug
    def test_foo(self):
        raise Exception("Bar")

    '''

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        def func():
            return f(*args, **kwargs)
        return DebugMode.run(func)

    return wrapper
