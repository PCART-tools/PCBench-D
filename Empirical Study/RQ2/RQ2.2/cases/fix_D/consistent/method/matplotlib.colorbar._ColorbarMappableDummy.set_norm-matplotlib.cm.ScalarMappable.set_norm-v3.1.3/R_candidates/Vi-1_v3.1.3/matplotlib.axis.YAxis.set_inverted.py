    def set_inverted(self, inverted):
        # docstring inherited
        a, b = self.get_view_interval()
        # cast to bool to avoid bad interaction between python 3.8 and np.bool_
        self.axes.set_ylim(sorted((a, b), reverse=bool(inverted)), auto=None)
