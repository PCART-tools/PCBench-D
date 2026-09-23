    @property
    def sp_values(self):
        # caching not an option, leaks memory
        return self.view(np.ndarray)
