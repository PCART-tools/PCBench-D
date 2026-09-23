    @classmethod
    def get_validators(cls):
        yield not_none_validator
        yield str_validator
        yield anystr_strip_whitespace
        yield anystr_length_validator
        yield cls.validate
