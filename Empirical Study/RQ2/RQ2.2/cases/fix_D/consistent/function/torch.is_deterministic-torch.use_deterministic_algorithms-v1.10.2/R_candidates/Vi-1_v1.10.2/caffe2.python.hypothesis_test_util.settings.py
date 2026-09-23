def settings(*args, **kwargs):
    if 'min_satisfying_examples' in kwargs and hypothesis.version.__version_info__ >= (3, 56, 0):
        kwargs.pop('min_satisfying_examples')

    if 'deadline' in kwargs and hypothesis.version.__version_info__ < (4, 44, 0):
        kwargs.pop('deadline')

    if 'timeout' in kwargs and hypothesis.version.__version_info__ >= (4, 44, 0):
        if 'deadline' not in kwargs:
            kwargs['deadline'] = kwargs['timeout'] * 1e3
        kwargs.pop('timeout')

    return hypothesis.settings(*args, **kwargs)
