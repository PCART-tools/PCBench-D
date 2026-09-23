    @classmethod
    def _result_converter(cls, values, na=None):
        return BooleanDtype().__from_arrow__(values)
