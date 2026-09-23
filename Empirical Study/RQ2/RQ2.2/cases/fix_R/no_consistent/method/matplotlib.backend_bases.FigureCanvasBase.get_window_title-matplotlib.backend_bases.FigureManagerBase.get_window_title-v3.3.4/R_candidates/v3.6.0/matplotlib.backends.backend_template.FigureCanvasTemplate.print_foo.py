    @_api.delete_parameter("3.5", "args")
    def print_foo(self, filename, *args, **kwargs):
        """
        Write out format foo.

        This method is normally called via `.Figure.savefig` and
        `.FigureCanvasBase.print_figure`, which take care of setting the figure
        facecolor, edgecolor, and dpi to the desired output values, and will
        restore them to the original values.  Therefore, `print_foo` does not
        need to handle these settings.
        """
        self.draw()
