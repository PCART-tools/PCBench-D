    def _copy_tick_props(self, src, dest):
        """Copy the properties from *src* tick to *dest* tick."""
        if src is None or dest is None:
            return
        dest.label1.update_from(src.label1)
        dest.label2.update_from(src.label2)
        dest.tick1line.update_from(src.tick1line)
        dest.tick2line.update_from(src.tick2line)
        dest.gridline.update_from(src.gridline)
        dest.update_from(src)
        dest._loc = src._loc
        dest._size = src._size
        dest._width = src._width
        dest._base_pad = src._base_pad
        dest._labelrotation = src._labelrotation
        dest._zorder = src._zorder
        dest._tickdir = src._tickdir
