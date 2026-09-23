    @final
    @classmethod
    def _string_data_error(cls, data):
        raise TypeError(
            "String dtype not supported, you may need "
            "to explicitly cast to a numeric type"
        )
