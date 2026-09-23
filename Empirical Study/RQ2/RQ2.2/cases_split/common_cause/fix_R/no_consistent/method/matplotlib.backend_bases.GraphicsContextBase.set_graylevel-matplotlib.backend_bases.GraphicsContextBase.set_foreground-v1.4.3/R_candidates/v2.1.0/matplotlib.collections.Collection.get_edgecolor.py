    def get_edgecolor(self):
        if (isinstance(self._edgecolors, six.string_types)
                   and self._edgecolors == str('face')):
            return self.get_facecolors()
        else:
            return self._edgecolors
