    @staticmethod
    def to_rgb(arg):
        """
        Returns an *RGB* tuple of three floats from 0-1.

        *arg* can be an *RGB* or *RGBA* sequence or a string in any of
        several forms:

            1) a letter from the set 'rgbcmykw'
            2) a hex color string, like '#00FFFF'
            3) a standard name, like 'aqua'
            4) a string representation of a float, like '0.4',
               indicating gray on a 0-1 scale

        if *arg* is *RGBA*, the *A* will simply be discarded.
        """
        return to_rgb(arg)
