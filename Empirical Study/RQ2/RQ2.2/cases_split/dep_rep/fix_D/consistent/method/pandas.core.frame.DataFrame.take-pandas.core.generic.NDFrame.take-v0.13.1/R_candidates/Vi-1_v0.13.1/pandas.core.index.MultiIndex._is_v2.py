    @property
    def _is_v2(self):
        contents = self.view(np.ndarray)
        return len(contents) > 0 and isinstance(contents[0], tuple)
