    @classmethod
    def get_validators(cls):
        if email_validator is None:
            raise ImportError('email-validator is not installed, run `pip install pydantic[email]`')

        yield str_validator
        yield cls.validate
