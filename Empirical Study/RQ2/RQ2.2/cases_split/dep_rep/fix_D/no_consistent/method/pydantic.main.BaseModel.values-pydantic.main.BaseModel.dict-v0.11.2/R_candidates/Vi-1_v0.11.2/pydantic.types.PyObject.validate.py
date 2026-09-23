    @classmethod
    def validate(cls, value):
        with change_exception(errors.PyObjectError, ImportError):
            return import_string(value)
