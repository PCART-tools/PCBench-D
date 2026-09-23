    @staticmethod
    def to_rgba_array(arg, alpha=None):
        """
        Returns a numpy array of *RGBA* tuples.

        Accepts a single mpl color spec or a sequence of specs.

        Special case to handle "no color": if *c* is "none" (case-insensitive),
        then an empty array will be returned.  Same for an empty list.
        """
        return to_rgba_array(arg, alpha)
