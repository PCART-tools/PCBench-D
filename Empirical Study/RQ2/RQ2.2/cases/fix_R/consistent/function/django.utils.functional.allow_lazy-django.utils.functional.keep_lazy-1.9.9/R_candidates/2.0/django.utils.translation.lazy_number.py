def lazy_number(func, resultclass, number=None, **kwargs):
    if isinstance(number, int):
        kwargs['number'] = number
        proxy = lazy(func, resultclass)(**kwargs)
    else:
        original_kwargs = kwargs.copy()

        class NumberAwareString(resultclass):
            def __bool__(self):
                return bool(kwargs['singular'])

            def __mod__(self, rhs):
                if isinstance(rhs, dict) and number:
                    try:
                        number_value = rhs[number]
                    except KeyError:
                        raise KeyError(
                            "Your dictionary lacks key '%s\'. Please provide "
                            "it, because it is required to determine whether "
                            "string is singular or plural." % number
                        )
                else:
                    number_value = rhs
                kwargs['number'] = number_value
                translated = func(**kwargs)
                try:
                    translated = translated % rhs
                except TypeError:
                    # String doesn't contain a placeholder for the number.
                    pass
                return translated

        proxy = lazy(lambda **kwargs: NumberAwareString(), NumberAwareString)(**kwargs)
        proxy.__reduce__ = lambda: (_lazy_number_unpickle, (func, resultclass, number, original_kwargs))
    return proxy
