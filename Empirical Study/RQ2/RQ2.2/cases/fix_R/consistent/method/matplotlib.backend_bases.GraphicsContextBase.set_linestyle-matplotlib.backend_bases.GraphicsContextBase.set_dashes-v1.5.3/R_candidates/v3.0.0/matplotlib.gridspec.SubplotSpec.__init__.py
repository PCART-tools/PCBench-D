    def __init__(self, gridspec, num1, num2=None):
        """
        The subplot will occupy the num1-th cell of the given
        gridspec.  If num2 is provided, the subplot will span between
        num1-th cell and num2-th cell.

        The index starts from 0.
        """
        self._gridspec = gridspec
        self.num1 = num1
        self.num2 = num2
        if gridspec._layoutbox is not None:
            glb = gridspec._layoutbox
            # So note that here we don't assign any layout yet,
            # just make the layoutbox that will conatin all items
            # associated w/ this axis.  This can include other axes like
            # a colorbar or a legend.
            self._layoutbox = layoutbox.LayoutBox(
                    parent=glb,
                    name=glb.name + '.ss' + layoutbox.seq_id(),
                    artist=self)
        else:
            self._layoutbox = None
