    def _auto_legend_data(self):
        """
        Returns list of vertices and extents covered by the plot.

        Returns a two long list.

        First element is a list of (x, y) vertices (in
        display-coordinates) covered by all the lines and line
        collections, in the legend's handles.

        Second element is a list of bounding boxes for all the patches in
        the legend's handles.
        """
        # should always hold because function is only called internally
        assert self.isaxes

        ax = self.parent
        bboxes = []
        lines = []
        offsets = []

        for handle in ax.lines:
            assert isinstance(handle, Line2D)
            path = handle.get_path()
            trans = handle.get_transform()
            tpath = trans.transform_path(path)
            lines.append(tpath)

        for handle in ax.patches:
            assert isinstance(handle, Patch)

            if isinstance(handle, Rectangle):
                transform = handle.get_data_transform()
                bboxes.append(handle.get_bbox().transformed(transform))
            else:
                transform = handle.get_transform()
                bboxes.append(handle.get_path().get_extents(transform))

        for handle in ax.collections:
            transform, transOffset, hoffsets, paths = handle._prepare_points()

            if len(hoffsets):
                for offset in transOffset.transform(hoffsets):
                    offsets.append(offset)

        try:
            vertices = np.concatenate([l.vertices for l in lines])
        except ValueError:
            vertices = np.array([])

        return [vertices, bboxes, lines, offsets]
