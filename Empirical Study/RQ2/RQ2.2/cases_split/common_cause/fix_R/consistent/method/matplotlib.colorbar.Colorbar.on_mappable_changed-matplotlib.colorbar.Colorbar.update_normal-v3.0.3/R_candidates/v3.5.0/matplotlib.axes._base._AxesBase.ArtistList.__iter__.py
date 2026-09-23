        def __iter__(self):
            for artist in self._axes._children:
                if self._type_check(artist):
                    yield artist
