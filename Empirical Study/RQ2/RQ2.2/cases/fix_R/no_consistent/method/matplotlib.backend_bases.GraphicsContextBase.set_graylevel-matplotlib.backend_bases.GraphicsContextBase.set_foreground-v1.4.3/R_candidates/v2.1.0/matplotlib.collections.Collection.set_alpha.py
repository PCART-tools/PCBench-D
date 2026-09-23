    def set_alpha(self, alpha):
        """
        Set the alpha tranparencies of the collection.  *alpha* must be
        a float or *None*.

        ACCEPTS: float or None
        """
        if alpha is not None:
            try:
                float(alpha)
            except TypeError:
                raise TypeError('alpha must be a float or None')
        self.update_dict['array'] = True
        artist.Artist.set_alpha(self, alpha)
        self._set_facecolor(self._original_facecolor)
        self._set_edgecolor(self._original_edgecolor)
