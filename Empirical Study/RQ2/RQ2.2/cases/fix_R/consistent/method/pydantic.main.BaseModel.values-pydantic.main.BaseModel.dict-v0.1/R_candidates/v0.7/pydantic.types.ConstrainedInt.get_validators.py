    @classmethod
    def get_validators(cls):
        yield int
        yield cls.validate
