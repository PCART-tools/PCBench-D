        def __len__(self):
            return sum(self._type_check(artist)
                       for artist in self._axes._children)
