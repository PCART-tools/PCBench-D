def indent_msg(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        args[0].indent += 1
        ret = fn(*args, **kwargs)
        args[0].indent -= 1
        return ret

    return wrapper
