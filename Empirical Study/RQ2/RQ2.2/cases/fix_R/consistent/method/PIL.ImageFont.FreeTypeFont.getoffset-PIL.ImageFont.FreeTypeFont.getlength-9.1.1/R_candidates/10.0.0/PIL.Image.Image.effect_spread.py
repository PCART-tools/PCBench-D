    def effect_spread(self, distance):
        """
        Randomly spread pixels in an image.

        :param distance: Distance to spread pixels.
        """
        self.load()
        return self._new(self.im.effect_spread(distance))
