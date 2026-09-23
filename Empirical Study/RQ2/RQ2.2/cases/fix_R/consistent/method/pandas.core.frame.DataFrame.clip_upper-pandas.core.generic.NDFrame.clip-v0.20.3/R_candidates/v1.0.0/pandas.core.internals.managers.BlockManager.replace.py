    def replace(self, value, **kwargs):
        assert np.ndim(value) == 0, value
        return self.apply("replace", value=value, **kwargs)
