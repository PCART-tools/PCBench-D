def hook_iterator(namespace, profile_name):

    def context():
        return torch.autograd.profiler.record_function(profile_name)

    class IteratorDecorator:
        '''Wrap the iterator return result by adding __next__'''
        def __init__(self, iterator):
            self.iterator = iterator

        def __iter__(self):
            return self

        def __next__(self):
            with context():
                return next(self.iterator)

    func = namespace['__iter__']

    if inspect.isgeneratorfunction(func):
        @functools.wraps(func)
        def wrap_generator(*args, **kwargs):
            gen = func(*args, **kwargs)
            try:
                with context():
                    response = gen.send(None)
                while True:
                    request = yield response
                    with context():
                        response = gen.send(request)
            except StopIteration as e:
                return e.value

        namespace['__iter__'] = wrap_generator
    else:
        if '__next__' in namespace:
            next_func = namespace['__next__']

            @functools.wraps(next_func)
            def wrap_next(*args, **kwargs):
                with context():
                    return next_func(*args, **kwargs)

            namespace['__next__'] = wrap_next
        else:
            # have the __iter__ but not __next__ like what _ChildDataPipe did.
            @functools.wraps(func)
            def wrap_iter(*args, **kwargs):
                iter_ret = func(*args, **kwargs)
                return IteratorDecorator(iter_ret)

            namespace['__iter__'] = wrap_iter
