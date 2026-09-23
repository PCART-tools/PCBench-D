    def set_color_cycle(self, clist):
        """
        Set the color cycle for any future plot commands on this Axes.

        *clist* is a list of mpl color specifiers.

        .. deprecated:: 1.5
        """
        cbook.warn_deprecated(
            '1.5', name='set_color_cycle', alternative='set_prop_cycle')
        if clist is None:
            # Calling set_color_cycle() or set_prop_cycle() with None
            # effectively resets the cycle, but you can't do
            # set_prop_cycle('color', None). So we are special-casing this.
            self.set_prop_cycle(None)
        else:
            self.set_prop_cycle('color', clist)
