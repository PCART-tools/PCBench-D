    @classmethod
    def get_validators(cls):
        yield str_validator
        yield cls.validate
