    @classmethod
    def validate(cls, value, values, **kwarg):
        if value:
            return value

        kwargs = {f: values.get(cls.prefix + f) for f in cls.fields}
        if kwargs['driver'] is None:
            raise errors.DSNDriverIsEmptyError()

        return make_dsn(**kwargs)
