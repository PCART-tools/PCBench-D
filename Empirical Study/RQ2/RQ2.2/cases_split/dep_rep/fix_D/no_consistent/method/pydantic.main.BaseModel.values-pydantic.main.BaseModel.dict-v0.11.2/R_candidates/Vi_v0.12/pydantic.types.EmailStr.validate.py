    @classmethod
    def validate(cls, value):
        return validate_email(value)[1]
