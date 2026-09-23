    @_api.deprecated("3.8", alternative="buffer_rgba")
    def tostring_rgb(self):
        return np.asarray(self._renderer).take([0, 1, 2], axis=2).tobytes()
