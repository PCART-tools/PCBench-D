    @classmethod
    def get_validators(cls):
        yield dict_validator
        yield cls.validate
