    def check(self, obj):
        return hasattr(obj, "dtype") and issubclass(obj.dtype.type, self.dtypes)
