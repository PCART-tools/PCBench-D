    @cbook.deprecated("2.1")
    def set_cursor_props(self, *args):
        """Set the cursor property as

        Call signature ::

          ax.set_cursor_props(linewidth, color)

        or::

          ax.set_cursor_props((linewidth, color))

        ACCEPTS: a (*float*, *color*) tuple
        """
        if len(args) == 1:
            lw, c = args[0]
        elif len(args) == 2:
            lw, c = args
        else:
            raise ValueError('args must be a (linewidth, color) tuple')
        c = mcolors.to_rgba(c)
        self._cursorProps = lw, c
