    @classmethod
    def parse_obj(cls, obj):
        if not isinstance(obj, dict):
            exc = TypeError(f'{cls.__name__} expected dict not {type(obj).__name__}')
            raise ValidationError([ErrorWrapper(exc, loc='__obj__')])
        return cls(**obj)
