    def get_matrix(self):
        if self._invalid:
            self._mtx = self._base_transform.get_matrix().copy()
            self._mtx[:2, -1] = 0
        return self._mtx
