    @classmethod
    def _simple_new(cls, values, name, **kwargs):
        result = values.view(cls)
        result.name = name
        return result
