    def get_window_extent(self, renderer=None):
        '''
        Return a :class:`~matplotlib.transforms.Bbox` object bounding
        the text and arrow annotation, in display units.

        *renderer* defaults to the _renderer attribute of the text
        object.  This is not assigned until the first execution of
        :meth:`draw`, so you must use this kwarg if you want
        to call :meth:`get_window_extent` prior to the first
        :meth:`draw`.  For getting web page regions, it is
        simpler to call the method after saving the figure. The
        *dpi* used defaults to self.figure.dpi; the renderer dpi is
        irrelevant.
        '''
        self.update_positions(renderer)
        if not self.get_visible():
            return Bbox.unit()

        text_bbox = Text.get_window_extent(self, renderer=renderer)
        bboxes = [text_bbox]

        if self.arrow_patch is not None:
            bboxes.append(
                self.arrow_patch.get_window_extent(renderer=renderer))

        return Bbox.union(bboxes)
