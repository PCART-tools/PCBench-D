    def _update_values(self):
        self._simplify_threshold = mpl.rcParams['path.simplify_threshold']
        self._should_simplify = (
            self._simplify_threshold > 0 and
            mpl.rcParams['path.simplify'] and
            len(self._vertices) >= 128 and
            (self._codes is None or np.all(self._codes <= Path.LINETO))
        )
