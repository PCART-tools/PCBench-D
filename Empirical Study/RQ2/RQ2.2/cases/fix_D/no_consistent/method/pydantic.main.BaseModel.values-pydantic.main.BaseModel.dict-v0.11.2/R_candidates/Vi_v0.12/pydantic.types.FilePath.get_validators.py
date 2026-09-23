    @classmethod
    def get_validators(cls):
        yield path_validator
        yield path_exists_validator
        yield cls.validate
