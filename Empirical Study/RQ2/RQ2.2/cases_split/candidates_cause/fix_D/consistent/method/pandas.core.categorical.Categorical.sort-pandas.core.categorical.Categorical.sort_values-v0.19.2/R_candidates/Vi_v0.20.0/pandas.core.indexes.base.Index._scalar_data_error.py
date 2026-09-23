    @classmethod
    def _scalar_data_error(cls, data):
        raise TypeError('{0}(...) must be called with a collection of some '
                        'kind, {1} was passed'.format(cls.__name__,
                                                      repr(data)))
