        def __iter__(self):
            for artist in list(self._axes._children):
                if self._type_check(artist):
                    yield artist
