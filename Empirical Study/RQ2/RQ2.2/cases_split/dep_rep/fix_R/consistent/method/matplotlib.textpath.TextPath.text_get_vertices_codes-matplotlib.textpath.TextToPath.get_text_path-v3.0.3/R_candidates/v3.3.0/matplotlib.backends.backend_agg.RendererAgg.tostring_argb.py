    def tostring_argb(self):
        return np.asarray(self._renderer).take([3, 0, 1, 2], axis=2).tobytes()
