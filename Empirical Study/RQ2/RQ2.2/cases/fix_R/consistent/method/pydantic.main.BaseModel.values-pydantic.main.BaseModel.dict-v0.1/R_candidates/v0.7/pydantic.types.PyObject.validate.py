    @classmethod
    def validate(cls, value):
        try:
            return import_string(value)
        except ImportError as e:
            # errors must be TypeError or ValueError
            raise ValueError(str(e)) from e
