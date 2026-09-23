    def _auto_legend_data(self):
        """
        Return display coordinates for hit testing for "best" positioning.

        Returns
        -------
        bboxes
            List of bounding boxes of all patches.
        lines
            List of `.Path` corresponding to each line.
        offsets
            List of (x, y) offsets of all collection.
        """
        assert self.isaxes  # always holds, as this is only called internally
        ax = self.parent
        lines = [line.get_transform().transform_path(line.get_path())
                 for line in ax.lines]
        bboxes = [patch.get_bbox().transformed(patch.get_data_transform())
                  if isinstance(patch, Rectangle) else
                  patch.get_path().get_extents(patch.get_transform())
                  for patch in ax.patches]
        offsets = []
        for handle in ax.collections:
            _, transOffset, hoffsets, _ = handle._prepare_points()
            for offset in transOffset.transform(hoffsets):
                offsets.append(offset)
        return bboxes, lines, offsets
