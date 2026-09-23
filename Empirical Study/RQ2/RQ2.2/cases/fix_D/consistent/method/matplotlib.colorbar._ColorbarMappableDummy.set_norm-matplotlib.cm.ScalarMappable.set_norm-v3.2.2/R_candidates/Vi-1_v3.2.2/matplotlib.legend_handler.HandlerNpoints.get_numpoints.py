    def get_numpoints(self, legend):
        if self._numpoints is None:
            return legend.numpoints
        else:
            return self._numpoints
