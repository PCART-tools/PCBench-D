    def __iter__(self):
        if  com.is_categorical_dtype(self.dtype):
            return iter(self.values)
        elif np.issubdtype(self.dtype, np.datetime64):
            return (lib.Timestamp(x) for x in self.values)
        elif np.issubdtype(self.dtype, np.timedelta64):
            return (lib.Timedelta(x) for x in self.values)
        else:
            return iter(self.values)
