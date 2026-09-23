    @classmethod
    def hatch(cls, hatchpattern, density=6):
        """
        Given a hatch specifier, *hatchpattern*, generates a Path that
        can be used in a repeated hatching pattern.  *density* is the
        number of lines per unit square.
        """
        from matplotlib.hatch import get_path

        if hatchpattern is None:
            return None

        hatch_path = cls._hatch_dict.get((hatchpattern, density))
        if hatch_path is not None:
            return hatch_path

        hatch_path = get_path(hatchpattern, density)
        cls._hatch_dict[(hatchpattern, density)] = hatch_path
        return hatch_path
