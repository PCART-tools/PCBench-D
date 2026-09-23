def argument_validation(f):
    signature = inspect.signature(f)
    hints = get_type_hints(f)

    @wraps(f)
    def wrapper(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        for argument_name, value in bound.arguments.items():
            if argument_name in hints and isinstance(hints[argument_name], _DataPipeMeta):
                hint = hints[argument_name]
                if not isinstance(value, IterDataPipe):
                    raise TypeError("Expected argument '{}' as a IterDataPipe, but found {}"
                                    .format(argument_name, type(value)))
                if not value.type.issubtype(hint.type):
                    raise TypeError("Expected type of argument '{}' as a subtype of "
                                    "hint {}, but found {}"
                                    .format(argument_name, hint.type, value.type))

        return f(*args, **kwargs)

    return wrapper
