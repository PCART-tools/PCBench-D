    def __iter__(self):
        """ provide iteration over the values of the Series
        box values if necessary """
        if is_datetimelike(self):
            return (_maybe_box_datetimelike(x) for x in self._values)
        else:
            return iter(self._values)
