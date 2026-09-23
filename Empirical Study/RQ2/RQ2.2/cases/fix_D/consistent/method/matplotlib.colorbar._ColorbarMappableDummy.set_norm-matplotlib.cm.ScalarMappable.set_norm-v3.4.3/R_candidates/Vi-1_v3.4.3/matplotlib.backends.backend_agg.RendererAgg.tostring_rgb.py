    def tostring_rgb(self):
        return np.asarray(self._renderer).take([0, 1, 2], axis=2).tobytes()
