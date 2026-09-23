def runtime_validation(f):
    # TODO:
    # Can be extended to validate '__getitem__' and nonblocking
    if f.__name__ != '__iter__':
        raise TypeError("Can not decorate function {} with 'runtime_validation'"
                        .format(f.__name__))

    @wraps(f)
    def wrapper(self):
        global _runtime_validation_enabled
        if not _runtime_validation_enabled:
            yield from f(self)
        else:
            it = f(self)
            for d in it:
                if not self.type.issubtype_of_instance(d):
                    raise RuntimeError("Expected an instance as subtype of {}, but found {}({})"
                                       .format(self.type, d, type(d)))
                yield d

    return wrapper
