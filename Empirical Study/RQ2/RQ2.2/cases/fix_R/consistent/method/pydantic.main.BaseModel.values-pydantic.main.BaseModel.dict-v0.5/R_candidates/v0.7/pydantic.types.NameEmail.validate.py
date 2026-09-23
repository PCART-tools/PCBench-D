    @classmethod
    def validate(cls, value):
        return cls(*validate_email(value))
