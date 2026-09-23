    @property
    def _is_v1(self):
        contents = self.view(np.ndarray)
        return len(contents) > 0 and not isinstance(contents[0], tuple)
