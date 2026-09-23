    def settings(*args, **kwargs):
        if 'min_satisfying_examples' in kwargs and hypothesis.version.__version_info__ >= (3, 56, 0):
            kwargs.pop('min_satisfying_examples')
        return hypothesis.settings(*args, **kwargs)
