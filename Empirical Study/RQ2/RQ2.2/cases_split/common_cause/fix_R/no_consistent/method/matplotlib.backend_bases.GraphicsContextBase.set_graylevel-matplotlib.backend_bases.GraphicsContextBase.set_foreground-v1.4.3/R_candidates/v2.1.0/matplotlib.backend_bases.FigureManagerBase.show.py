    def show(self):
        """
        For GUI backends, show the figure window and redraw.
        For non-GUI backends, raise an exception to be caught
        by :meth:`~matplotlib.figure.Figure.show`, for an
        optional warning.
        """
        raise NonGuiException()
