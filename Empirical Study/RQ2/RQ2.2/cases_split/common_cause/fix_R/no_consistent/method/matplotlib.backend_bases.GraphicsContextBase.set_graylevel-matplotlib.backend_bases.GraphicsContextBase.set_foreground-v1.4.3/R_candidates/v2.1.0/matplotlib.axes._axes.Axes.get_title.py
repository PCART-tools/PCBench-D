    def get_title(self, loc="center"):
        """Get an axes title.

        Get one of the three available axes titles. The available titles
        are positioned above the axes in the center, flush with the left
        edge, and flush with the right edge.

        Parameters
        ----------
        loc : {'center', 'left', 'right'}, str, optional
            Which title to get, defaults to 'center'

        Returns
        -------
        title: str
            The title text string.

        """
        try:
            title = {'left': self._left_title,
                     'center': self.title,
                     'right': self._right_title}[loc.lower()]
        except KeyError:
            raise ValueError("'%s' is not a valid location" % loc)
        return title.get_text()
