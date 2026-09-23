    def _get_tick_boxes_siblings(self, xdir, renderer):
        """
        Get the bounding boxes for this `.axis` and its siblings
        as set by `.Figure.align_xlabels` or  `.Figure.align_ylablels`.

        By default it just gets bboxes for self.
        """
        raise NotImplementedError('Derived must override')
