    @staticmethod
    def _homogenize_dict(self, frames, intersect=True, dtype=None):
        """
        Conform set of _constructor_sliced-like objects to either
        an intersection of indices / columns or a union.

        Parameters
        ----------
        frames : dict
        intersect : boolean, default True

        Returns
        -------
        dict of aligned results & indicies
        """

        result = dict()
        # caller differs dict/ODict, presered type
        if isinstance(frames, OrderedDict):
            result = OrderedDict()

        adj_frames = OrderedDict()
        for k, v in compat.iteritems(frames):
            if isinstance(v, dict):
                adj_frames[k] = self._constructor_sliced(v)
            else:
                adj_frames[k] = v

        axes = self._AXIS_ORDERS[1:]
        axes_dict = dict([(a, ax) for a, ax in zip(axes, self._extract_axes(
            self, adj_frames, axes, intersect=intersect))])

        reindex_dict = dict(
            [(self._AXIS_SLICEMAP[a], axes_dict[a]) for a in axes])
        reindex_dict['copy'] = False
        for key, frame in compat.iteritems(adj_frames):
            if frame is not None:
                result[key] = frame.reindex(**reindex_dict)
            else:
                result[key] = None

        axes_dict['data'] = result
        axes_dict['dtype'] = dtype
        return axes_dict
