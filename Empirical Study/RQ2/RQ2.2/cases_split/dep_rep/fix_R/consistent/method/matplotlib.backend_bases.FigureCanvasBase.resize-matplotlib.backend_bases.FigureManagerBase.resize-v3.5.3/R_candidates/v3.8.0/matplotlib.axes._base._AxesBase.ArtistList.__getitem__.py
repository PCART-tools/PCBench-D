        def __getitem__(self, key):
            return [artist
                    for artist in self._axes._children
                    if self._type_check(artist)][key]
