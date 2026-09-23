    @staticmethod
    @lru_cache(8)
    def hatch(hatchpattern, density=6):
        """
        Given a hatch specifier, *hatchpattern*, generates a `Path` that
        can be used in a repeated hatching pattern.  *density* is the
        number of lines per unit square.
        """
        from matplotlib.hatch import get_path
        return (get_path(hatchpattern, density)
                if hatchpattern is not None else None)
