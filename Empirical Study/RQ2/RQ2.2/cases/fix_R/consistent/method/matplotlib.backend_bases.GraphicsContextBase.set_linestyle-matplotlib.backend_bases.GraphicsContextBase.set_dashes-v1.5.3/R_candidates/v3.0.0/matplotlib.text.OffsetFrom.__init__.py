    def __init__(self, artist, ref_coord, unit="points"):
        '''
        Parameters
        ----------
        artist : `Artist`, `BboxBase`, or `Transform`
            The object to compute the offset from.

        ref_coord : length 2 sequence
            If `artist` is an `Artist` or `BboxBase`, this values is
            the location to of the offset origin in fractions of the
            `artist` bounding box.

            If `artist` is a transform, the offset origin is the
            transform applied to this value.

        unit : {'points, 'pixels'}
            The screen units to use (pixels or points) for the offset
            input.

        '''
        self._artist = artist
        self._ref_coord = ref_coord
        self.set_unit(unit)
