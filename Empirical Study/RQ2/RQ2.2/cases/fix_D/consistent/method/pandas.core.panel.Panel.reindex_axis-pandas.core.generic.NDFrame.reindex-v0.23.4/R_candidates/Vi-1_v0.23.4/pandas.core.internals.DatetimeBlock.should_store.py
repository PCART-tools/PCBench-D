    def should_store(self, value):
        return (issubclass(value.dtype.type, np.datetime64) and
                not is_datetimetz(value))
