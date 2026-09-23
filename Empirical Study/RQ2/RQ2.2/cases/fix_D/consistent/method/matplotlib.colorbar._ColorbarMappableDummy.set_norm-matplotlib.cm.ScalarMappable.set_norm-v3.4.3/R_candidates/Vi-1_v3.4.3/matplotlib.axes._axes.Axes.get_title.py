    def get_title(self, loc="center"):
        """
        Get an Axes title.

        Get one of the three available Axes titles. The available titles
        are positioned above the Axes in the center, flush with the left
        edge, and flush with the right edge.

        Parameters
        ----------
        loc : {'center', 'left', 'right'}, str, default: 'center'
            Which title to return.

        Returns
        -------
        str
            The title text string.

        """
        titles = {'left': self._left_title,
                  'center': self.title,
                  'right': self._right_title}
        title = _api.check_getitem(titles, loc=loc.lower())
        return title.get_text()
