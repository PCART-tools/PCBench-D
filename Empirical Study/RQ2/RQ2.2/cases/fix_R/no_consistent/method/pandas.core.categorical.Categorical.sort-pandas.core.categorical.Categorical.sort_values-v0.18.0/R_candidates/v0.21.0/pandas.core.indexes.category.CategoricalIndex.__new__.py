    def __new__(cls, data=None, categories=None, ordered=None, dtype=None,
                copy=False, name=None, fastpath=False, **kwargs):

        if fastpath:
            return cls._simple_new(data, name=name, dtype=dtype)

        if name is None and hasattr(data, 'name'):
            name = data.name

        if isinstance(data, ABCCategorical):
            data = cls._create_categorical(cls, data, categories, ordered,
                                           dtype)
        elif isinstance(data, CategoricalIndex):
            data = data._data
            data = cls._create_categorical(cls, data, categories, ordered,
                                           dtype)
        else:

            # don't allow scalars
            # if data is None, then categories must be provided
            if is_scalar(data):
                if data is not None or categories is None:
                    cls._scalar_data_error(data)
                data = []
            data = cls._create_categorical(cls, data, categories, ordered)

        if copy:
            data = data.copy()

        return cls._simple_new(data, name=name)
