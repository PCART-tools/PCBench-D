    @classmethod
    def get_validators(cls):
        yield not_none_validator
        yield decimal_validator
        yield number_size_validator
        yield cls.validate
