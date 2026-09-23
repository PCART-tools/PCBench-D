    def format_coord(self, theta, r):
        """
        Return a format string formatting the coordinate using Unicode
        characters.
        """
        if theta < 0:
            theta += 2 * np.pi
        theta /= np.pi
        return ('\N{GREEK SMALL LETTER THETA}=%0.3f\N{GREEK SMALL LETTER PI} '
                '(%0.3f\N{DEGREE SIGN}), r=%0.3f') % (theta, theta * 180.0, r)
