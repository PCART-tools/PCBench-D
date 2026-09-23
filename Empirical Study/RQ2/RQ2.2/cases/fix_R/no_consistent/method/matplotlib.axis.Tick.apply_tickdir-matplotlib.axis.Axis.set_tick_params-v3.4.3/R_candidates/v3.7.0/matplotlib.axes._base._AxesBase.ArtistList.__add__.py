        def __add__(self, other):
            if isinstance(other, (list, _AxesBase.ArtistList)):
                return [*self, *other]
            if isinstance(other, (tuple, _AxesBase.ArtistList)):
                return (*self, *other)
            return NotImplemented
