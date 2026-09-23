    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        """
        Draw the text instance

        Parameters
        ----------
        gc : `GraphicsContextBase`
            the graphics context

        x : scalar
            the x location of the text in display coords

        y : scalar
            the y location of the text baseline in display coords

        s : str
            the text string

        prop : `matplotlib.font_manager.FontProperties`
            font properties

        angle : scalar
            the rotation angle in degrees

        mtext : `matplotlib.text.Text`
            the original text object to be rendered

        Notes
        -----
        **backend implementers note**

        When you are trying to determine if you have gotten your bounding box
        right (which is what enables the text layout/alignment to work
        properly), it helps to change the line in text.py::

            if 0: bbox_artist(self, renderer)

        to if 1, and then the actual bounding box will be plotted along with
        your text.
        """

        self._draw_text_as_path(gc, x, y, s, prop, angle, ismath)
