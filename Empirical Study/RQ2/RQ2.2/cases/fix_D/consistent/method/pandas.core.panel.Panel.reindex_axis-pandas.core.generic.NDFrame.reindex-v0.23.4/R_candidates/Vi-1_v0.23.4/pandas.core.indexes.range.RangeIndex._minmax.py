    def _minmax(self, meth):
        no_steps = len(self) - 1
        if no_steps == -1:
            return np.nan
        elif ((meth == 'min' and self._step > 0) or
              (meth == 'max' and self._step < 0)):
            return self._start

        return self._start + self._step * no_steps
