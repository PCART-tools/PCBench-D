def print_stderr(*args, **kwargs):
    kwargs['file'] = sys.stderr
    return print(*args, **kwargs)
