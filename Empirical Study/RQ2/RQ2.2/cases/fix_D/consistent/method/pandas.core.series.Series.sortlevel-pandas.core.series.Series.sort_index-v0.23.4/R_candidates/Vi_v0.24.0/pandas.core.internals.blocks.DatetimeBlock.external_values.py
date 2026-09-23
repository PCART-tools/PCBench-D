    def external_values(self):
        return np.asarray(self.values.astype('datetime64[ns]', copy=False))
