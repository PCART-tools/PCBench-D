    def check(self, obj) -> bool:
        return hasattr(obj, "dtype") and issubclass(obj.dtype.type, self.dtypes)
