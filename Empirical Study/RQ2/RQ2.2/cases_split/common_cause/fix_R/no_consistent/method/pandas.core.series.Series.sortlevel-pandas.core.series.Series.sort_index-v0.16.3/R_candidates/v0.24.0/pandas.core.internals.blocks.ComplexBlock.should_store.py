    def should_store(self, value):
        return issubclass(value.dtype.type, np.complexfloating)
