    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Clipping has not been implemented in the OffesetBox family, so
        # disable the clip flag for consistency. It can always be turned back
        # on to zero effect.
        self.set_clip_on(False)

        self._children = []
        self._offset = (0, 0)
